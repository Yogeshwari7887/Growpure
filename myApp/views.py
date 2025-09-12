from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, Vegie, Fruit, Pulse, User
from django.contrib import messages
from .models import ContactMessage

def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = sum(order.total_price for order in Order.objects.all())
    total_products = Vegie.objects.count() + Fruit.objects.count() + Pulse.objects.count()
    recent_orders = Order.objects.order_by('-order_date')[:5]

    # Fetch recent customer queries
    customer_queries = ContactMessage.objects.order_by('-submitted_at')[:5]  # Get last 5 queries

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'recent_orders': recent_orders,
        'customer_queries': customer_queries,  # Send queries to template
    }
    return render(request, 'admin_panel/dashboard.html', context)

def manage_orders(request):
    orders = Order.objects.all().order_by('-order_date')
    return render(request, 'admin_panel/manage_orders.html', {'orders': orders})

def get_order_items(self):
    return "<br>".join([f"{item.product_name} (Qty: {item.quantity})" for item in self.order_items.all()])

def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/manage_users.html', {'users': users})

def manage_products(request):
    vegies = Vegie.objects.all()
    fruits = Fruit.objects.all()
    pulses = Pulse.objects.all()
    products = list(vegies) + list(fruits) + list(pulses)
    return render(request, 'admin_panel/manage_products.html', {
        'products': products,
        'vegies': vegies,
        'fruits': fruits,
        'pulses': pulses
    })

def add_product(request):
    if request.method == "POST":
        title = request.POST["title"]
        price = request.POST["price"]
        category = request.POST["category"]
        photo = request.FILES["photo"]

        if category == "vegie":
            Vegie.objects.create(title=title, price=price, photo=photo)
        elif category == "fruit":
            Fruit.objects.create(title=title, price=price, photo=photo)
        elif category == "pulse":
            Pulse.objects.create(title=title, price=price, photo=photo)

        return redirect("manage_products")  # Redirect to manage products after adding

    return render(request, "admin_panel/add_product.html")

def edit_product(request, category, product_id):
    # Mapping category to model
    model_map = {
        "vegie": Vegie,
        "fruit": Fruit,
        "pulse": Pulse
    }

    model = model_map.get(category)
    if not model:
        messages.error(request, "Invalid product category!")
        return redirect("manage_products")

    # Fetch the correct product
    product = get_object_or_404(model, id=product_id)

    if request.method == "POST":
        product.title = request.POST.get("title", product.title)
        product.price = request.POST.get("price", product.price)

        if "photo" in request.FILES:
            product.photo = request.FILES["photo"]

        product.save()
        messages.success(request, "Product updated successfully!")
        return redirect("manage_products")

    return render(request, "admin_panel/edit_product.html", {"product": product, "category": category})



def delete_product(request, product_id):
    product = None

    # Check in all models
    if Vegie.objects.filter(id=product_id).exists():
        product = get_object_or_404(Vegie, id=product_id)
    elif Fruit.objects.filter(id=product_id).exists():
        product = get_object_or_404(Fruit, id=product_id)
    elif Pulse.objects.filter(id=product_id).exists():
        product = get_object_or_404(Pulse, id=product_id)

    if product:
        product.delete()
        messages.success(request, "Product deleted successfully!")

    return redirect("manage_products")

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if user.is_superuser:  # Prevent deleting admin
        messages.error(request, "You cannot delete an admin user!")
    else:
        user.delete()
        messages.success(request, "User deleted successfully!")

    return redirect("manage_users")

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.username = request.POST["username"]
        user.email = request.POST["email"]
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.save()
        messages.success(request, "User details updated successfully!")
        return redirect("manage_users")

    return render(request, "admin_panel/edit_user.html", {"user": user})  # ✅ Corrected template path

def add_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password = request.POST["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            messages.success(request, "User created successfully!")
            return redirect("manage_users")

    return render(request, "admin_panel/add_user.html")

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, "Order canceled successfully!")
    return redirect("manage_orders")

def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        order.full_name = request.POST["full_name"]
        order.email = request.POST["email"]
        order.phone = request.POST["phone"]
        order.address = request.POST["address"]
        order.city = request.POST["city"]
        order.state = request.POST["state"]
        order.zip_code = request.POST["zip_code"]
        order.payment_method = request.POST["payment_method"]
        order.save()
        messages.success(request, "Order updated successfully!")
        return redirect("manage_orders")

    return render(request, "admin_panel/edit_order.html", {"order": order})

def manage_feedback(request):
    feedbacks = ContactMessage.objects.all().order_by('-submitted_at')  # Latest first
    return render(request, 'admin_panel/admin_feedback.html', {'feedbacks': feedbacks})

def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(ContactMessage, id=feedback_id)
    feedback.delete()
    messages.success(request, "Feedback deleted successfully!")
    return redirect('manage_feedback')
