from django.shortcuts import render , redirect , get_object_or_404
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.paginator import Paginator
from myApp.models import Fruit  , Pulse , Vegie , ContactMessage ,Wishlist  ,Cart ,Order , User , MyFarm , Coupon , Producer , Cow , Farmer , BlogPost
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import update_session_auth_hash
import logging
from decimal import Decimal
from django.db.models import Q

#===================================LINK TO Views =======================

def home(request):
    return render(request, 'hero.html')

def upper(request):
    return render(request, 'upper.html')

def bottom(request):
    return render(request, 'footer.html')

def success(request):
    return render(request, 'success.html')

def login(request):
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def shop(request):
    return render(request, 'shop.html')

def register(request):
    return render(request, 'register.html')

# def contact(request):
#     return render(request, 'contact.html')

def this404(request):
    return render(request, '404.html')

def checkout(request):
    return render(request, 'checkout.html')

def blog(request):
    return render(request, 'blog.html')

def cart(request):
    return render(request, 'cart.html')

def product(request):
    return render(request, 'product-details.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def success(request):
    return render(request, 'success.html') 

def products(request):
    return render(request , 'products.html')

def hotpicks(request):
    return render(request ,'hotpicks.html')

#======================================== DATABASE VIEWS ===============================================

def fruit_page(request):
    return render(request, 'fruit_list.html')

def pulses(request):
    return render(request, 'pulses.html')

def fruit_list(request):
    fruits = Fruit.objects.all()
    return render(request, 'fruit_list.html', {'fruits': fruits})  

def pulse_list(request):
    pulses = Pulse.objects.all()  # Fetch all pulses from the database
    return render(request, 'pulse_store.html', {'pulses': pulses})

def vegie_list(request):
    vegies = Vegie.objects.all()  # Fetch all records from Vegie model
    return render(request, 'vegie.html', {'vegies': vegies})  # Pass data to template

#========================================= CONTACT DATA ===========================================

def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        # Show success message
        messages.success(request, "Your message has been sent successfully!")

        return redirect('/success/')  # Redirect to a success page

    return render(request, 'contact.html')

#========================================= ADD to Wishlist ===========================

@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_fruit_to_wishlist(request, fruit_id):
    fruit = get_object_or_404(Fruit, id=fruit_id)
    Wishlist.objects.get_or_create(user=request.user, fruit=fruit)
    return redirect('fruit')

@login_required
def add_pulse_to_wishlist(request, pulse_id):
    pulse = get_object_or_404(Pulse, id=pulse_id)
    Wishlist.objects.get_or_create(user=request.user, pulse=pulse)
    return redirect('pulse_list')

@login_required
def add_vegie_to_wishlist(request, vegie_id):
    vegie = get_object_or_404(Vegie, id=vegie_id)
    Wishlist.objects.get_or_create(user=request.user, vegie=vegie)
    return redirect('vegie-list')

@login_required
def remove_from_wishlist(request, wishlist_id):
    wishlist_item = get_object_or_404(Wishlist, id=wishlist_id, user=request.user)
    wishlist_item.delete()
    return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirects back to the same page

#==================== ADD to Cart =================================

def add_to_cart(request, product_type, product_id):
    if product_type == 'fruit':
        product = get_object_or_404(Fruit, id=product_id)
    elif product_type == 'vegie':
        product = get_object_or_404(Vegie, id=product_id)
    elif product_type == 'pulse':
        product = get_object_or_404(Pulse, id=product_id)
    else:
        messages.error(request, "Invalid product type")
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    cart_item, created = Cart.objects.get_or_create(
        product_type=product_type,
        product_id=product.id,
        defaults={'title': product.title, 'price': product.price, 'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"✅ {product.title} added to cart successfully!")

    return redirect(request.META.get('HTTP_REFERER', 'home'))  # Redirects back to the same page


def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.delete()
    return redirect('cart_view')

def clear_cart(request):
    Cart.objects.all().delete()
    return redirect('cart_view')


def increase_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def decrease_quantity(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()  # Remove item if quantity reaches 0
    return redirect('cart_view')

#==================== Checkout ============================

def checkout_view(request):
    cart_items = Cart.objects.all()
    total_price = sum(Decimal(item.price) * item.quantity for item in cart_items)

    # Retrieve rounded discount amount from session
    discount_amount = Decimal(str(request.session.get('discount_amount', '0'))).quantize(Decimal('0.00'))

    # Apply Coupon if available
    coupon_discount = Decimal('0')
    applied_coupon = None
    if 'coupon_code' in request.session:
        try:
            applied_coupon = Coupon.objects.get(code=request.session['coupon_code'])
            coupon_discount = Decimal(applied_coupon.discount).quantize(Decimal('0.00'))
        except Coupon.DoesNotExist:
            del request.session['coupon_code']

    # Calculate Final Price (rounded to 2 decimal places)
    final_price = (total_price - discount_amount - coupon_discount).quantize(Decimal('0.00'))

    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip_code = request.POST['zip_code']
        payment_method = request.POST['payment_method']

        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect('cart_view')

        # Create order summary details
        order_summary = [
            {"title": item.title, "quantity": item.quantity, "price": float(item.price)}
            for item in cart_items
        ]

        # Create Order
        order = Order.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            payment_method=payment_method,
            total_price=final_price,
            order_items=json.dumps(order_summary),
            discount_amount=discount_amount,
            coupon_discount=coupon_discount,
            coupon_code=applied_coupon.code if applied_coupon else None
        )

        # Clear cart and session after checkout
        Cart.objects.all().delete()
        request.session.pop('discount_amount', None)  # Remove discount from session
        request.session.pop('coupon_code', None)  # Remove coupon code from session

        messages.success(request, "Order placed successfully!")
        return redirect('order_success')

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price.quantize(Decimal('0.00')),
        'discount_amount': discount_amount,
        'coupon_discount': coupon_discount,
        'applied_coupon': applied_coupon,
        'final_price': final_price
    })


def order_success(request):
    latest_order = Order.objects.latest('id')  # Fetch the last placed order
    return render(request, 'order_success.html', {'order': latest_order})

#================================ Track Order ==============================


def track_order(request):
    order = None
    error = None

    if request.method == "POST":
        order_id = request.POST.get("order_id")
        contact_info = request.POST.get("contact_info")

        try:
            order = Order.objects.get(id=order_id)
            if order.email != contact_info and order.phone != contact_info:
                error = "Invalid Order ID or Contact Information."
                order = None
        except Order.DoesNotExist:
            error = "Order not found."

    return render(request, "track_order.html", {"order": order, "error": error})

#--------------------------- User DASHBOARD =========================================


@login_required
def user_dashboard(request):
    orders = Order.objects.filter(email=request.user.email).order_by('-order_date')
    wishlist_items = Wishlist.objects.filter(user=request.user)

    context = {
        'title': 'User Dashboard',  # ✅ Add this line
        'orders': orders,
        'wishlist_items': wishlist_items
    }
    return render(request, 'admin_panel/user_dashboard.html', context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(email=request.user.email).order_by('-order_date')
    return render(request, 'admin_panel/my_orders.html', {'orders': orders})

@login_required
def edit_account(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        user.username = username
        user.email = email

        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)  # Keep the user logged in after password change

        user.save()
        messages.success(request, "Account updated successfully!")
        return redirect('user_dashboard')

    return render(request, 'admin_panel/user_dashboard.html')

def user_orders(request):
    orders = Order.objects.filter(user=request.user)
    
    for order in orders:
        order_items = []
        for item in order.order_items.all():  # Ensure you have a related field for order items
            order_items.append({
                "name": item.product.title,  # Adjust field names as per your model
                "quantity": item.quantity,
                "price": item.product.price
            })
        
        # Convert the list to a JSON string for embedding in HTML
        order.items_json = json.dumps(order_items)

    return render(request, 'user_dashboard.html', {'orders': orders})

#=====================================================================================

def cart_view(request):
    cart_items = Cart.objects.all()
    total_price = sum(Decimal(item.price) * item.quantity for item in cart_items)

    # Define discount tiers
    discount_tiers = {
        250: Decimal('0.02'),  # 2% discount at ₹250
        500: Decimal('0.05'),  # 5% discount at ₹500
        750: Decimal('0.07'),  # 7% discount at ₹750
        1000: Decimal('0.10')  # 10% discount at ₹1000
    }

    discount_amount = Decimal('0')
    next_discount_threshold = None

    for threshold, discount in sorted(discount_tiers.items()):
        if total_price >= threshold:
            discount_amount = total_price * discount
        elif next_discount_threshold is None:
            next_discount_threshold = threshold - total_price

    # Round discount amount to 2 decimal places before storing in session
    request.session['discount_amount'] = float(round(discount_amount, 2))

    # Handle Coupon Application
    applied_coupon = None
    coupon_discount = Decimal('0')
    if 'coupon_code' in request.session:
        try:
            applied_coupon = Coupon.objects.get(code=request.session['coupon_code'])
            coupon_discount = Decimal(applied_coupon.discount)
        except Coupon.DoesNotExist:
            del request.session['coupon_code']

    # Calculate Final Price
    final_price = total_price - discount_amount - coupon_discount

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'discount_amount': round(discount_amount, 2),  # Ensure rounding in template
        'next_discount_threshold': next_discount_threshold,
        'applied_coupon': applied_coupon,
        'coupon_discount': coupon_discount,
        'final_price': round(final_price, 2)  # Ensure final price is also rounded
    })


def apply_coupon(request):
    if request.method == 'POST':
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(code=coupon_code)
            request.session['coupon_code'] = coupon_code
            messages.success(request, f"Coupon '{coupon_code}' applied successfully!")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code!")

    return redirect('cart_view')

#===============================================================================

def coupon_list(request):
    """Display all available coupons in the admin dashboard."""
    coupons = Coupon.objects.all()
    return render(request, 'admin_panel/coupon_list.html', {'coupons': coupons})

def add_coupon(request):
    """Add a new coupon through a simple form submission."""
    if request.method == "POST":
        code = request.POST.get('code')
        discount = request.POST.get('discount')

        if Coupon.objects.filter(code=code).exists():
            messages.error(request, "Coupon code already exists!")
        else:
            Coupon.objects.create(code=code, discount=discount)
            messages.success(request, "Coupon added successfully!")
            return redirect('coupon_list')

    return render(request, 'admin_panel/add_coupon.html')

def edit_coupon(request, coupon_id):
    """Edit an existing coupon."""
    coupon = get_object_or_404(Coupon, id=coupon_id)

    if request.method == "POST":
        coupon.code = request.POST.get('code')
        coupon.discount = request.POST.get('discount')
        coupon.save()
        messages.success(request, "Coupon updated successfully!")
        return redirect('coupon_list')

    return render(request, 'admin_panel/edit_coupon.html', {'coupon': coupon})

def delete_coupon(request, coupon_id):
    """Delete a coupon from the system."""
    coupon = get_object_or_404(Coupon, id=coupon_id)
    coupon.delete()
    messages.success(request, "Coupon deleted successfully!")
    return redirect('coupon_list')

#========================= FARM MANAGEMENT ===================================

#===========================myfarm=========================

def myfarm_list(request):
    farms = MyFarm.objects.all()  # Fetch all farm entries
    return render(request, 'farm/myfarm_list.html', {'farms':farms})

#========================farmer=============

def farmer_list(request):
    farmers = Farmer.objects.all()
    print(farmers)  # Debugging output
    return render(request, 'farm/farmer_list.html', {'farmers': farmers})


#==========================produceer===================

def producer_list(request):
    producers = Producer.objects.all()  # Fetch all farm entries
    return render(request, 'farm/producer_list.html', {'producers':producers})

#===================================cows====================

def cow_list(request):
    cows = Cow.objects.all()  # Fetch all farm entries
    return render(request, 'farm/cow_list.html', {'cows':cows})

#================================== Blog ===================

def blog_list(request):
    query = request.GET.get('q')  # Get the search query from URL parameters
    posts = BlogPost.objects.all().order_by('-created_at')  # Get all posts

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |  # Search in title
            Q(category__icontains=query) |  # Search in category
            Q(content__icontains=query)  # Search in content
        )

    # Pagination - 6 posts per page
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')  # Get the current page number
    page_obj = paginator.get_page(page_number)  # Get paginated page object

    return render(request, 'blog/blog_list.html', {'page_obj': page_obj, 'query': query})

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/blog_detail.html', {'post': post})