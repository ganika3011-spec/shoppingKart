from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product
from .models import Cart, CartItem
from django.http import HttpResponse as httpResponse
from django.core.exceptions import ObjectDoesNotExist
from store.models import Variation
from django.contrib.auth.decorators import login_required

# Create your views here.

def _cart_id(request):
    cart= request.session.session_key
    if not cart:
        cart= request.session.create()
    return cart

def add_cart(request,product_id):
    current_user= request.user
    product= Product.objects.get(id= product_id) #get the product
    # if the user is authenticated
    if current_user.is_authenticated:
        product_variation= []
        if request.method == 'POST':
           for item in request.POST:
               key= item
               value= request.POST[key]

               try:
                   variation= Variation.objects.get(product= product, variation_category__iexact= key, variation_value__iexact= value)
                   product_variation.append(variation)
               except:
                   pass
        is_cart_item_exists= CartItem.objects.filter(product= product, user= current_user).exists()
        if is_cart_item_exists:
           cart_item= CartItem.objects.filter(product= product, user= current_user )
        # existing variation-> database
        # current variation -> product-variation
        # item_id -> database,
           ex_var_list= []
           id= []
           for item in cart_item:
               existing_variation= item.variations.all()
               ex_var_list.append(list(existing_variation))
               id.append(item.id)
           if product_variation in ex_var_list:
              index= ex_var_list.index(product_variation)
              item_id= id[index]
              item= CartItem.objects.get(product= product, id= item_id)
              item.quantity += 1
              item.save()
           else:
              item = CartItem.objects.create(
                product= product,
                quantity= 1,
                user= current_user,
             )

              if len(product_variation) > 0:
                 item.variations.clear()
                 item.variations.add(*product_variation)
        #cart_item.quantity += 1
              item.save()
        else :
            cart_item= CartItem.objects.create(
            product= product,
            quantity= 1,
            user= current_user,
            
        )
            if len(product_variation) > 0:
               cart_item.variations.clear()
               cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')

    
    else:
        product_variation = []
        if request.method == 'POST':
           for item in request.POST:
               key= item
               value= request.POST[key]

               try:
                   variation= Variation.objects.get(product= product, variation_category__iexact= key, variation_value__iexact= value)
                   product_variation.append(variation)
               except:
                     pass
        try:
            cart= Cart.objects.get(cart_id= _cart_id(request)) #get the cart using the cart_id present in the session
        except Cart.DoesNotExist:
            cart= Cart.objects.create(
                cart_id= _cart_id(request)
            )
            cart.save()

        is_cart_item_exists= CartItem.objects.filter(product= product,cart=cart).exists()
        if is_cart_item_exists:
           cart_item= CartItem.objects.filter(product= product, cart= cart)
        # existing variation-> database
        # current variation -> product-variation
        # item_id -> database,
           ex_var_list= []
           id= []
           for item in cart_item:
               existing_variation= item.variations.all()
               ex_var_list.append(list(existing_variation))
               id.append(item.id)
           print(ex_var_list)

           if product_variation in ex_var_list:
              index= ex_var_list.index(product_variation)
              item_id= id[index]
              item= CartItem.objects.get(product= product, id= item_id)
              item.quantity += 1
              item.save()
           else:
              item = CartItem.objects.create(
                product= product,
                quantity= 1,
                cart=cart,
             )

              if len(product_variation) > 0:
                 item.variations.clear()
                 item.variations.add(*product_variation)
        #cart_item.quantity += 1
              item.save()
        else :
            cart_item= CartItem.objects.create(
            product= product,
            quantity= 1,
            cart=cart,
            
        )
            if len(product_variation) > 0:
               cart_item.variations.clear()
               cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart')
    

def remove_cart(request, product_id,cart_item_id):
    
    product= get_object_or_404(Product, id= product_id)
    try:
        if request.user.is_authenticated:
            cart_item= CartItem.objects.get(product= product, user= request.user, id= cart_item_id)
        else:
            cart= Cart.objects.get(cart_id= _cart_id(request))
            cart_item= CartItem.objects.get(product= product, cart= cart, id= cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

from django.http import JsonResponse

def update_cart_ajax(request):
    """Update cart quantities via AJAX."""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    product_id = request.POST.get('product_id')
    cart_item_id = request.POST.get('cart_item_id')
    action = request.POST.get('action') # 'add' or 'remove'
    
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(id=cart_item_id, user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(id=cart_item_id, cart=cart)
            
        if action == 'add':
            # Check stock
            if cart_item.product.stock > cart_item.quantity:
                cart_item.quantity += 1
                cart_item.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'Out of stock'}, status=400)
        elif action == 'remove':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
                return JsonResponse({'status': 'removed'})
                
        # Recalculate totals
        total = 0
        quantity = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
            
        tax = (2 * total) / 100
        grand_total = total + tax
        
        return JsonResponse({
            'status': 'success',
            'quantity': cart_item.quantity if action != 'remove' or cart_item.pk else 0,
            'sub_total': f"{cart_item.sub_total():.2f}",
            'total': f"{total:.2f}",
            'tax': f"{tax:.2f}",
            'grand_total': f"{grand_total:.2f}",
            'cart_count': quantity,
        })
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def remove_cart_item(request, product_id,cart_item_id):
    
    product= get_object_or_404(Product, id= product_id)
    if request.user.is_authenticated:
        cart_item= CartItem.objects.get(product= product, user= request.user, id= cart_item_id)
    else:
        cart= Cart.objects.get(cart_id= _cart_id(request))
        cart_item= CartItem.objects.get(product= product, cart= cart, id= cart_item_id)
    cart_item.delete()
    return redirect('cart')                        
    
def cart(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        Grand_total=0
        if request.user.is_authenticated:
            cart_items= CartItem.objects.filter(user= request.user, is_active= True)
        else:
            cart= Cart.objects.get(cart_id= _cart_id(request))
            cart_items= CartItem.objects.filter(cart= cart, is_active= True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax= (2 * total)/100
        Grand_total= total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    
    context= {
        'total': total, 
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'Grand_total': Grand_total,
    }
    return render(request,"store/cart.html",context)
@login_required(login_url= 'login')
def checkout(request,total=0,quantity=0,cart_items=None):
    try:
        tax=0
        Grand_total=0
        if request.user.is_authenticated:
            cart_items= CartItem.objects.filter(user= request.user, is_active= True)
        else:
            cart= Cart.objects.get(cart_id= _cart_id(request))
            cart_items= CartItem.objects.filter(cart= cart, is_active= True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax= (2 * total)/100
        Grand_total= total + tax
    except ObjectDoesNotExist:
        pass #just ignore
    
    context= {
        'total': total, 
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'Grand_total': Grand_total,
    }
    return render(request,"store/checkout.html",context)