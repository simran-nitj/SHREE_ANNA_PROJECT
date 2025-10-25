# marketplace/views.py


from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
# marketplace/views.py
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm # Import Django's form
from django.contrib import messages # To show success messages
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
# marketplace/views.py

# marketplace/views.py

def product_list(request):
    # Start with all products, ordered by the newest first (this part is the same)
    products_list = Product.objects.all().order_by('-listed_on')
    
    # --- Search Logic (this part is the same) ---
    search_query = request.GET.get('query', None)
    if search_query:
        products_list = products_list.filter(
            Q(millet_name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )

    # --- Filter Logic (this part is the same) ---
    millet_filter = request.GET.get('millet_type', None)
    if millet_filter and millet_filter != "":
        products_list = products_list.filter(millet_name__iexact=millet_filter)

    # --- Pagination Logic (this is the new part) ---
    # Create a Paginator object, showing 6 products per page
    paginator = Paginator(products_list, 6) 
    # Get the page number from the URL (e.g., /?page=2)
    page_number = request.GET.get('page')
    # Get the Page object for the requested page number
    products = paginator.get_page(page_number)

    # Get a unique list of all millet types for the dropdown menu
    millet_types = Product.objects.values_list('millet_name', flat=True).distinct().order_by('millet_name')

    context = {
        'products': products, # Pass the paginated products to the template
        'millet_types': millet_types,
    }
    return render(request, 'marketplace/product_list.html', context)
    



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



def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Get the cart from the session, or create an empty dictionary if it doesn't exist
    cart = request.session.get('cart', {})
    product_id_str = str(product.id)

    # For simplicity, we'll just add one of each item.
    # A more advanced cart would handle quantity.
    cart[product_id_str] = {'quantity': 1} 

    request.session['cart'] = cart
    messages.success(request, f'"{product.millet_name}" was added to your cart.')
    return redirect('cart_detail')


def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, item_data in cart.items():
        product = get_object_or_404(Product, id=int(product_id))
        item_total = product.price_per_kg * item_data['quantity']
        cart_items.append({
            'product': product,
            'quantity': item_data['quantity'],
            'total': item_total,
        })
        total_price += item_total

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'marketplace/cart_detail.html', context)
# marketplace/views.py

def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    quantity = int(request.POST.get('quantity', 1)) # Get quantity from the form

    if quantity > 0:
        cart[product_id_str] = {'quantity': quantity}
        messages.success(request, 'Cart updated successfully.')
    else:
        # If quantity is 0 or less, remove the item
        if product_id_str in cart:
            del cart[product_id_str]
            messages.success(request, 'Item removed from cart.')

    request.session['cart'] = cart
    return redirect('cart_detail')
# marketplace/views.py

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        messages.success(request, 'Item removed from cart.')

    request.session['cart'] = cart
    return redirect('cart_detail')