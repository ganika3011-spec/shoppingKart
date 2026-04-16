from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Variation, ReviewRating, ProductGallery, Wishlist
import admin_thumbnails
from Kart.ai_utils import generate_product_description


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    """Inline admin for product gallery."""
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Admin interface for Product model."""
    
    list_display = (
        'product_name',
        'category',
        'price_display',
        'stock_status',
        'is_available',
        'average_review_display',
        'created_date',
    )
    list_filter = (
        'is_available',
        'category',
        'created_date',
        'modified_date',
    )
    search_fields = ('product_name', 'description', 'slug')
    prepopulated_fields = {'slug': ('product_name',)}
    list_editable = ('is_available',)
    readonly_fields = ('created_date', 'modified_date', 'average_review_display', 'review_count_display')
    
    fieldsets = (
        ('General Information', {
            'fields': ('product_name', 'slug', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'is_available')
        }),
        ('Description', {
            'fields': ('description',),
            'classes': ('wide',)
        }),
        ('Media', {
            'fields': ('image',),
        }),
        ('Reviews & Ratings', {
            'fields': ('average_review_display', 'review_count_display'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_date', 'modified_date'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ProductGalleryInline]
    
    def price_display(self, obj):
        """Display price with currency formatting."""
        return f"${obj.price:.2f}"
    price_display.short_description = 'Price'
    
    def stock_status(self, obj):
        """Display stock status with color coding."""
        if obj.stock > 10:
            color = 'green'
            status = 'In Stock'
        elif obj.stock > 0:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'red'
            status = 'Out of Stock'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            status
        )
    stock_status.short_description = 'Stock Status'
    
    def average_review_display(self, obj):
        """Display average review rating."""
        avg = obj.average_review
        return f"{avg:.1f} ⭐" if avg > 0 else "No ratings"
    average_review_display.short_description = 'Average Rating'
    
    def review_count_display(self, obj):
        """Display total review count."""
        return f"{obj.review_count} reviews"
    review_count_display.short_description = 'Review Count'
    
    actions = ['mark_as_available', 'mark_as_unavailable', 'generate_ai_description']

    def generate_ai_description(self, request, queryset):
        """Bulk action to generate AI descriptions for products."""
        success_count = 0
        for product in queryset:
            description = generate_product_description(product.product_name, product.category.category_name)
            if "AI features are currently disabled" not in description and "Sorry, I encountered an error" not in description:
                product.description = description
                product.save()
                success_count += 1
        
        if success_count > 0:
            self.message_user(request, f"Successfully generated AI descriptions for {success_count} products.")
        else:
            self.message_user(request, "Failed to generate AI descriptions. Please check your API key and network connection.", level='error')
    generate_ai_description.short_description = "Generate AI descriptions"
    
    def mark_as_available(self, request, queryset):
        """Bulk action to mark products as available."""
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} products marked as available.")
    mark_as_available.short_description = "Mark selected as available"
    
    def mark_as_unavailable(self, request, queryset):
        """Bulk action to mark products as unavailable."""
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} products marked as unavailable.")
    mark_as_unavailable.short_description = "Mark selected as unavailable"


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    """Admin interface for Variation model."""
    
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
        'created_date',
    )
    list_filter = (
        'variation_category',
        'is_active',
        'created_date',
    )
    search_fields = (
        'product__product_name',
        'variation_value',
    )
    list_editable = ('is_active',)
    readonly_fields = ('created_date',)
    
    fieldsets = (
        ('Variation Details', {
            'fields': ('product', 'variation_category', 'variation_value', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_date',),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['activate_variations', 'deactivate_variations']
    
    def activate_variations(self, request, queryset):
        """Bulk action to activate variations."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} variations activated.")
    activate_variations.short_description = "Activate selected variations"
    
    def deactivate_variations(self, request, queryset):
        """Bulk action to deactivate variations."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} variations deactivated.")
    deactivate_variations.short_description = "Deactivate selected variations"


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    """Admin interface for ReviewRating model."""
    
    list_display = (
        'subject',
        'user',
        'product',
        'rating_display',
        'status',
        'created_at',
    )
    list_filter = (
        'status',
        'rating',
        'created_at',
    )
    search_fields = (
        'subject',
        'user__username',
        'product__product_name',
        'review',
    )
    list_editable = ('status',)
    readonly_fields = ('user', 'product', 'ip', 'created_at', 'updated_at')
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'user', 'subject', 'review')
        }),
        ('Rating', {
            'fields': ('rating', 'status')
        }),
        ('Meta Information', {
            'fields': ('ip', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'reject_reviews']
    
    def rating_display(self, obj):
        """Display rating with star emojis."""
        stars = '⭐' * int(obj.rating)
        return f"{stars} ({obj.rating})"
    rating_display.short_description = 'Rating'
    
    def approve_reviews(self, request, queryset):
        """Bulk action to approve reviews."""
        updated = queryset.update(status=True)
        self.message_user(request, f"{updated} reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def reject_reviews(self, request, queryset):
        """Bulk action to reject reviews."""
        updated = queryset.update(status=False)
        self.message_user(request, f"{updated} reviews rejected.")
    reject_reviews.short_description = "Reject selected reviews"


@admin_thumbnails.thumbnail('image')
@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    """Admin interface for ProductGallery model."""
    
    list_display = ('product', 'image_thumb')
    list_filter = ('product',)
    search_fields = ('product__product_name',)
    
    fieldsets = (
        ('Gallery Item', {
            'fields': ('product', 'image')
        }),
    )
    
    def image_thumb(self, obj):
        """Display thumbnail of the image."""
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" />',
                obj.image.url
            )
        return "No image"
    image_thumb.short_description = 'Thumbnail'


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    """Admin interface for Wishlist model."""
    
    list_display = ('user', 'product_count_display', 'updated_date')
    list_filter = ('created_date', 'updated_date')
    search_fields = ('user__username', 'user__email', 'products__product_name')
    filter_horizontal = ('products',)
    readonly_fields = ('created_date', 'updated_date')
    
    fieldsets = (
        ('User & Date', {
            'fields': ('user', 'created_date', 'updated_date')
        }),
        ('Products', {
            'fields': ('products',),
            'description': 'Select products to add to this wishlist'
        }),
    )
    
    def product_count_display(self, obj):
        """Display number of products in wishlist."""
        count = obj.product_count()
        return format_html(
            '<span style="background: #007bff; color: white; padding: 4px 12px; border-radius: 4px;">{}</span>',
            count
        )
    product_count_display.short_description = 'Products'
