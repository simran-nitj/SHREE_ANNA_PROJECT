# marketplace/views.py


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
# marketplace/views.py

from django.contrib.auth.forms import UserCreationForm # Import Django's form
from django.contrib import messages # To show success messages
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
def product_list(request):
    products = Product.objects.all().order_by('-listed_on')
    return render(request, 'marketplace/product_list.html', {'products': products})

# --- Add this new function ---
def product_detail(request, pk):
    # This gets the single product with the matching pk (primary key/id).
    # If no product is found, it will show a "Page Not Found" error.
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'marketplace/product_detail.html', {'product': product})
# --- Add this new function ---
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login') # This line will now work
    else:
        form = UserCreationForm()
    return render(request, 'marketplace/register.html', {'form': form})
# marketplace/views.py

@login_required # This decorator protects the view
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES) # request.FILES for the image
        if form.is_valid():
            # Don't save the form to the database yet.
            product = form.save(commit=False)
            # Assign the currently logged-in user as the farmer.
            product.farmer = request.user
            # Now save the product with the farmer info.
            product.save()
            messages.success(request, 'Your product has been listed successfully!')
            return redirect('product_list') # Redirect to homepage
    else:
        form = ProductForm()
    return render(request, 'marketplace/product_form.html', {'form': form})
# marketplace/views.py

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Security check: Ensure the user trying to edit is the product's owner
    if product.farmer != request.user:
        messages.error(request, 'You are not authorized to edit this product.')
        return redirect('product_list')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your product has been updated!')
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'marketplace/product_form.html', {'form': form, 'title': 'Update Product'})

# marketplace/views.py

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    # Security check
    if product.farmer != request.user:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('product_list')

    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Your product has been deleted.')
        return redirect('product_list')

    return render(request, 'marketplace/product_confirm_delete.html', {'product': product})