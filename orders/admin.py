from django.contrib import admin
from .models import Order, OrderProduct,Payments


# Register your models here.
@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount_paid', 'status', 'created_at')
    search_fields = ('payment_id', 'user__email')
    list_filter = ('status', 'created_at')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'first_name', 'last_name', 'order_total', 'status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'user__email', 'first_name', 'last_name')
    list_filter = ('status', 'is_ordered', 'created_at')
    list_per_page= 20

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'product_price', 'ordered', 'created_at')
    search_fields = ('order__order_number', 'product__product_name')
    list_filter = ('ordered', 'created_at')