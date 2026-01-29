from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display= ('product_name','price','stock','category','is_available','created_date','modified_date')
    prepopulated_fields= {'slug':('product_name',)}
    list_editable= ('is_available','stock')
    search_fields= ('product_name',)
    list_filter= ('is_available','created_date','modified_date')

# Register your models here.
