from django.contrib import admin
from .models import Product, Scheme  # <-- 1. Add 'Scheme' to this import line

# Register your models here.
admin.site.register(Product)
admin.site.register(Scheme)     # <-- 2. Add this new line to register Scheme