
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
]
