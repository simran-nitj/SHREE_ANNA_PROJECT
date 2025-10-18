from django.db import models
from django.contrib.auth.models import User # Imports Django's built-in User model

# Create your models here.

class Product(models.Model):
    # This links the product to a specific user (the farmer).
    # If a user is deleted, all their products are also deleted (CASCADE).
    farmer = models.ForeignKey(User, on_delete=models.CASCADE)

    # The name of the millet, like "Ragi" or "Jowar".
    millet_name = models.CharField(max_length=100)

    # The quantity available, in kilograms.
    quantity_kg = models.FloatField()

    # The price for one kilogram. We use DecimalField for money to be accurate.
    price_per_kg = models.DecimalField(max_digits=10, decimal_places=2)

    # A longer description of the product.
    description = models.TextField()

    # An image of the product. The images will be saved in a folder called 'product_images'.
    image = models.ImageField(upload_to='product_images/')

    # A timestamp that is automatically set when a product is first listed.
    listed_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.millet_name} by {self.farmer.username}"