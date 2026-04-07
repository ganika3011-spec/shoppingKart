from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from category.models import Category
from accounts.models import Account


class Product(models.Model):
    """Product model representing items in the store."""
    
    product_name = models.CharField(max_length=200, unique=True, db_index=True)
    slug = models.SlugField(max_length=200, unique=True, db_index=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(upload_to='photos/products/')
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        default=0
    )
    is_available = models.BooleanField(default=True, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-created_date']
        indexes = [
            models.Index(fields=['is_available', 'category']),
            models.Index(fields=['created_date']),
        ]

    def __str__(self):
        return self.product_name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])

    @property
    def average_review(self):
        """Get average rating for this product."""
        reviews = ReviewRating.objects.filter(
            product=self,
            status=True
        ).aggregate(average=Avg('rating'))
        return round(float(reviews['average'] or 0), 2)

    @property
    def review_count(self):
        """Get total number of reviews for this product."""
        return ReviewRating.objects.filter(
            product=self,
            status=True
        ).count()

    def is_in_stock(self):
        """Check if product is available in stock."""
        return self.stock > 0


VARIATION_CHOICES = (
    ('color', 'Color'),
    ('size', 'Size'),
)


class VariationManager(models.Manager):
    """Custom manager for Variation model."""
    
    def colors(self):
        return self.filter(variation_category='color', is_active=True)

    def sizes(self):
        return self.filter(variation_category='size', is_active=True)


class Variation(models.Model):
    """Product variations like size and color."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variations'
    )
    variation_category = models.CharField(
        max_length=100,
        choices=VARIATION_CHOICES
    )
    variation_value = models.CharField(max_length=100, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManager()

    class Meta:
        verbose_name = 'Variation'
        verbose_name_plural = 'Variations'
        unique_together = ('product', 'variation_category', 'variation_value')
        indexes = [
            models.Index(fields=['product', 'variation_category']),
        ]

    def __str__(self):
        return f"{self.product.product_name} - {self.variation_value}"


class ReviewRating(models.Model):
    """User reviews and ratings for products."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ip = models.GenericIPAddressField(blank=True, null=True)
    status = models.BooleanField(default=False)  # Admin approval needed
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Review Rating'
        verbose_name_plural = 'Review Ratings'
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product', 'status']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.subject} - {self.user.username}" if self.subject else f"Review by {self.user.username}"


class ProductGallery(models.Model):
    """Product gallery images."""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery'
    )
    image = models.ImageField(upload_to='photos/products/gallery/', max_length=255)

    class Meta:
        verbose_name = 'Product Gallery'
        verbose_name_plural = 'Product Galleries'

    def __str__(self):
        return f"Gallery for {self.product.product_name}"


class Wishlist(models.Model):
    """Wishlist model to save favorite products."""
    
    user = models.OneToOneField(
        Account,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    products = models.ManyToManyField(Product, related_name='wishlisted_by')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'
        ordering = ['-updated_date']

    def __str__(self):
        return f"Wishlist for {self.user.username}"

    def product_count(self):
        return self.products.count()