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
# marketplace/models.py

class Scheme(models.Model):
    name = models.CharField(max_length=255, help_text="Official name of the scheme")
    description = models.TextField(help_text="Detailed description of the scheme's benefits")
    eligibility = models.TextField(help_text="Who is eligible for this scheme (e.g., small farmers, SHGs)")
    documents_required = models.TextField(help_text="List of documents needed to apply")
    official_link = models.URLField(max_length=500, blank=True)
    # We add this field for the AI to easily search
    keywords = models.TextField(help_text="Comma-separated keywords (e.g., tractor, subsidy, loan, maharashtra)")

    def __str__(self):
        return self.name