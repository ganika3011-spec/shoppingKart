from django.contrib import admin
from .models import Product,Variation

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ('product_name','price','stock','category','is_available','created_date','modified_date')
    prepopulated_fields= {'slug':('product_name',)}
    list_editable= ('is_available','stock')
    search_fields= ('product_name',)
    list_filter= ('is_available','created_date','modified_date')

@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display= ('product','variation_category','variation_value','is_active','created_date')
    list_editable= ('is_active',)
    list_filter= ('variation_category','is_active')
    search_fields= ('product__product_name',)

# Register your models here.
