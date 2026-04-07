from django.urls import path
from . import views 

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.login, name='login'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name='resetpassword_validate'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('change_password/', views.change_password, name='change_password'),
    path('order_detail/<int:order_id>/', views.order_detail, name='order_detail'),
   # path("reset-password/<uidb64>/<token>/", views.reset_password, name="reset_password"),
    #path('logout/', views.logout_view, name='logout'),
    #path('register/', views.register_view, name='register'),
    #path('profile/', views.profile_view, name='profile'),
]