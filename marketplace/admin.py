from django.contrib import admin
from .models import Product  # Import the Product model we created

# Register your models here.

# This simple line tells Django to make the Product model
# manageable in the admin interface.
admin.site.register(Product)