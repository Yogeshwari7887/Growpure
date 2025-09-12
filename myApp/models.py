from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
import json
from decimal import Decimal

class Vegie(models.Model):
    photo = models.ImageField(upload_to="vegie/")
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Fruit(models.Model):
    photo = models.ImageField(upload_to="fruits/")
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class Pulse(models.Model):
    photo = models.ImageField(upload_to="pulse/")
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title
    
#======================== Contact ====================

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"
    

#======================= ADD TO Wishlist ====================

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE, null=True, blank=True)
    pulse = models.ForeignKey(Pulse, on_delete=models.CASCADE, null=True, blank=True)
    vegie = models.ForeignKey(Vegie, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        if self.fruit:
            return f"{self.user.username} - {self.fruit.title} (Fruit)"
        elif self.pulse:
            return f"{self.user.username} - {self.pulse.title} (Pulse)"
        elif self.vegie:
            return f"{self.user.username} - {self.vegie.title} (Vegie)"
        
#======================= ADD to CART ======================

class Cart(models.Model):
    product_type = models.CharField(max_length=50)  # 'fruit', 'vegie', or 'pulse'
    product_id = models.IntegerField()  # Stores the ID of the product
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.title} - {self.quantity}"
    
#===================== Checkout ==============================

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('UPI', 'UPI Payment'),
        ('CARD', 'Credit/Debit Card'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    order_items = models.JSONField(default=list)  # Proper JSON storage

    # ✅ ADD THESE FIELDS
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    coupon_discount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    coupon_code = models.CharField(max_length=50, blank=True, null=True)


    def get_order_items_display(self):
        """Parse order_items JSON and return formatted string."""
        try:
            items = json.loads(self.order_items) if isinstance(self.order_items, str) else self.order_items
            print("Loaded order items:", items)  # Debugging
            return "<br>".join([f"{item.get('product_name', 'Unknown Product')} (Qty: {item.get('quantity', 0)})" for item in items])
        except (json.JSONDecodeError, TypeError) as e:
            print("Error parsing order items:", e)  # Debugging
            return "No valid order items available"

    def __str__(self):
        return f"Order #{self.id} - {self.full_name} - {self.status}"

#=============================== Coupen System =============

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code
    
#============================== Farm management ====================
#==================myfarm=====================


class MyFarm(models.Model):
    title = models.CharField(max_length=200,default="Default Farm Title")  # Title of the cow
    video = models.FileField(upload_to='cow_videos/', blank=True, null=True,default='default_video.mp4')  # Field to upload video (optional)
    description = models.TextField(default="Default description")  # Description of the cow
    photos1 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')
    photos2 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')
    photos3 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for when the cow entry is created


    def _str_(self):
        return self.title

#==================================farmer===============================

class Farmer(models.Model):
    title = models.CharField(max_length=200,default="Default Farm Title")  # Title of the cow
    photos1 = models.ImageField(upload_to='farmer_photos1/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    description1  = models.TextField(default="Default description")  # Description of the cow
    photos2 = models.ImageField(upload_to='farmer_photos2/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    photos3 = models.ImageField(upload_to='farmer_photos3/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    description2 = models.TextField(default="Default description")  # Description of the cow
    video1 = models.FileField(upload_to='farmer_videos1/', blank=True, null=True,default='default_video.mp4')  # Field to upload video (optional)
    description3 = models.TextField(default="Default description")  # Description of the cow
    photos4 = models.ImageField(upload_to='farmer_photos4/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    photos5 = models.ImageField(upload_to='farmer_photos5/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    description4 = models.TextField(default="Default description")  # Description of the cow
    photos6 = models.ImageField(upload_to='farmer_photos6/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    description5 = models.TextField(default="Default description")  # Description of the cow
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for when the cow entry is created


    def __str__(self):
        return self.title

#=========================================producers================================

class Producer(models.Model):
    title = models.CharField(max_length=200,default="Default Farm Title")  # Title of the cow
    photos11 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    description = models.TextField(default="Default description")  # Description of the cow
    photos12 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    video = models.FileField(upload_to='cow_videos/', blank=True, null=True,default='default_video.mp4')  # Field to upload video (optional)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for when the cow entry is created

    def _str_(self):
        return self.title

#================================cow============================================

class Cow(models.Model):
    title = models.CharField(max_length=200,default="Default Farm Title")  # Title of the cow
    photos11 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    description = models.TextField(default="Default description")  # Description of the cow
    photos12 = models.ImageField(upload_to='cow_photos/', blank=True, null=True,default='default_photo.jpg')  # Field to upload photos (optional)
    video = models.FileField(upload_to='cow_videos/', blank=True, null=True,default='default_video.mp4')  # Field to upload video (optional)
    created_at = models.DateTimeField(default=timezone.now)  # Timestamp for when the cow entry is created

    def _str_(self):
        return self.title
    
#=============================== Blog =========================================

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    category = models.CharField(max_length=100, choices=[
        ('Organic Farming', 'Organic Farming'),
        ('Health & Nutrition', 'Health & Nutrition'),
        ('Sustainability', 'Sustainability'),
        ('News', 'News'),
    ])
    tags = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title