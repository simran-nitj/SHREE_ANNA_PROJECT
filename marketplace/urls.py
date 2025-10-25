
# marketplace/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    # Add this new URL for the registration page
    path('register/', views.register, name='register'),
    path('product/new/', views.product_create, name='product_create'),

    # Add this new URL for updating a product
    path('product/<int:pk>/update/', views.product_update, name='product_update'),
    # Add this new URL for deleting a product
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    # Add these two new URLs for the cart
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    path('api/ask-bot/', views.ai_bot_query, name='ai_bot_query'),

]
