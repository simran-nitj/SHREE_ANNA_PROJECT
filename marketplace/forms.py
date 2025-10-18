# marketplace/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # We don't want the user to choose the farmer,
        # so we exclude it from the form.
        fields = ['millet_name', 'quantity_kg', 'price_per_kg', 'description', 'image']
        