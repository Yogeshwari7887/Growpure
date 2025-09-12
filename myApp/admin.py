from django.contrib import admin
from .models import  Vegie , Fruit , Pulse ,ContactMessage , Cart , Order , MyFarm , Coupon ,Producer, Farmer , Cow , BlogPost

admin.site.register(Vegie)
admin.site.register(Fruit)
admin.site.register(Pulse)
admin.site.register(Cart)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'total_price', 'status', 'order_date')
    list_filter = ('status', 'order_date')
    search_fields = ('full_name', 'email', 'phone')
    list_editable = ('status',)  # Allows admin to change order status directly

admin.site.register(Order, OrderAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')  # Columns in the list view
    search_fields = ('name', 'email', 'message')  # Search functionality
    list_filter = ('submitted_at',)  # Filter messages by date
    readonly_fields = ('name', 'email', 'message', 'submitted_at')  # Make fields read-only

admin.site.register(ContactMessage, ContactMessageAdmin)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount')
    search_fields = ('code',)

#====================== Farm MANAGEMENT =================================


@admin.register(MyFarm)
class MyFarmAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  # Fields shown in admin list view
    search_fields = ('title', 'description')  # Searchable fields
    list_filter = ('created_at',)  # Filters on the side

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')  
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(Producer)
class ProducerAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

@admin.register(Cow)
class CowAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)

#============================ Blog ===============================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'category')
    prepopulated_fields = {'slug': ('title',)}