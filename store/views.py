"""
Store views for product listing, details, search, and reviews.
"""

import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Prefetch
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings

from category.models import Category
from .models import Product, ReviewRating
from .forms import ReviewForm
from carts.models import CartItem
from carts.views import _cart_id
from orders.models import OrderProduct

logger = logging.getLogger(__name__)
ITEMS_PER_PAGE = getattr(settings, 'ITEMS_PER_PAGE', 12)


@require_http_methods(["GET"])
def store(request, category_slug=None):
    """
    Display all products or filter by category.
    
    Args:
        request: HTTP request object
        category_slug: Optional category slug for filtering
        
    Returns:
        Rendered store template with paginated products
    """
    try:
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(
                category=category,
                is_available=True
            ).select_related('category')
        else:
            products = Product.objects.filter(
                is_available=True
            ).select_related('category').order_by('-created_date')

        # Pagination
        paginator = Paginator(products, ITEMS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        
        try:
            paged_products = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            paged_products = paginator.page(1)
            logger.warning(f"Invalid page number: {page_number}")

        context = {
            'products': paged_products,
            'product_count': products.count(),
            'category': category_slug,
        }
        return render(request, 'store/store.html', context)
        
    except Category.DoesNotExist:
        messages.error(request, "Category not found.")
        return redirect('store')
    except Exception as e:
        logger.error(f"Error in store view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading products.")
        return redirect('home')


@require_http_methods(["GET"])
def product_detail(request, category_slug, product_slug):
    """
    Display detailed information about a specific product.
    
    Args:
        request: HTTP request object
        category_slug: Category slug of the product
        product_slug: Product slug
        
    Returns:
        Rendered product detail template
    """
    try:
        # Use select_related for foreign key optimization
        product = Product.objects.select_related('category').get(
            slug=product_slug,
            category__slug=category_slug
        )
        
        # Check if product is in cart
        in_cart = CartItem.objects.filter(
            cart__cart_id=_cart_id(request),
            product=product
        ).exists()
        
        # Check if user has purchased this product
        user_purchased = False
        if request.user.is_authenticated:
            user_purchased = OrderProduct.objects.filter(
                user=request.user,
                product=product
            ).exists()
        
        # Get approved reviews with prefetch optimization
        reviews = product.reviews.filter(status=True).select_related('user')

        context = {
            'single_product': product,
            'product': product,
            'in_cart': in_cart,
            'user_purchased': user_purchased,
            'reviews': reviews,
            'average_rating': product.average_review,
            'review_count': product.review_count,
        }
        
        return render(request, 'store/product_detail.html', context)
        
    except Product.DoesNotExist:
        logger.info(f"Product not found: {category_slug}/{product_slug}")
        messages.error(request, "Product not found.")
        return redirect('store')
    except Exception as e:
        logger.error(f"Error in product_detail view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while loading the product.")
        return redirect('store')


@require_http_methods(["GET"])
def search(request):
    """
    Search for products by keyword in name or description.
    
    Args:
        request: HTTP request object with 'keyword' GET parameter
        
    Returns:
        Rendered store template with search results
    """
    products = Product.objects.none()
    product_count = 0
    keyword = ''
    
    try:
        keyword = request.GET.get('keyword', '').strip()
        
        if keyword:
            if len(keyword) < 2:
                messages.warning(request, "Search term must be at least 2 characters long.")
            else:
                # Use Q objects for OR queries
                products = Product.objects.filter(
                    Q(product_name__icontains=keyword) |
                    Q(description__icontains=keyword) |
                    Q(category__category_name__icontains=keyword),
                    is_available=True
                ).select_related('category').order_by('-created_date')
                
                product_count = products.count()
                logger.info(f"Search performed: '{keyword}' - {product_count} results")
        
        # Pagination
        paginator = Paginator(products, ITEMS_PER_PAGE)
        page_number = request.GET.get('page', 1)
        
        try:
            paged_products = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            paged_products = paginator.page(1)

        context = {
            'products': paged_products,
            'product_count': product_count,
            'keyword': keyword,
        }
        
        return render(request, 'store/store.html', context)
        
    except Exception as e:
        logger.error(f"Error in search view: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred during search.")
        return redirect('store')


@login_required(login_url='login')
@require_http_methods(["POST"])
def submit_review(request, product_id):
    """
    Submit or update a product review.
    
    Args:
        request: HTTP request object with form data
        product_id: ID of the product being reviewed
        
    Returns:
        Redirect to referrer or product detail page
    """
    referrer = request.META.get('HTTP_REFERER', 'store')
    
    try:
        product = get_object_or_404(Product, id=product_id)
        
        # Try to get existing review
        try:
            review = ReviewRating.objects.get(
                user=request.user,
                product=product
            )
            is_new = False
        except ReviewRating.DoesNotExist:
            review = ReviewRating(user=request.user, product=product)
            is_new = True
        
        form = ReviewForm(request.POST, instance=review)
        
        if form.is_valid():
            review_obj = form.save(commit=False)
            review_obj.ip = _get_client_ip(request)
            review_obj.status = False  # Requires admin approval
            review_obj.save()
            
            if is_new:
                messages.success(
                    request,
                    "Thank you! Your review has been submitted and is pending approval."
                )
                logger.info(f"New review submitted by {request.user.username} for product {product_id}")
            else:
                messages.success(request, "Your review has been updated.")
                logger.info(f"Review updated by {request.user.username} for product {product_id}")
        else:
            messages.error(request, "Please correct the errors in the form.")
            logger.warning(f"Invalid review form submission: {form.errors}")
        
        return redirect(referrer)
        
    except Product.DoesNotExist:
        logger.error(f"Product not found: {product_id}")
        messages.error(request, "Product not found.")
        return redirect(referrer)
    except Exception as e:
        logger.error(f"Error in submit_review: {str(e)}", exc_info=True)
        messages.error(request, "An error occurred while submitting your review.")
        return redirect(referrer)


def _get_client_ip(request):
    """
    Get client IP address from request.
    
    Args:
        request: HTTP request object
        
    Returns:
        Client IP address string
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

