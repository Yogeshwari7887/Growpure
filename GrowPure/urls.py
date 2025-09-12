from django.contrib import admin
from django.urls import path , include
from GrowPure import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [

#================================= BASIC LINKS TO BE ACCESSED =====================

    path('admin/', admin.site.urls),
    path('',views.home, name='home'),
    path('home/',views.home, name='home'),
    path('about/', views.about, name='about'),
    # path('blog/', views.blog, name='blog'),
    path('shop/', views.shop, name='shop'),
    path('product-details/', views.product, name='product-details'),
    path('404/', views.about, name='404'),
    path('success/', views.success, name='success'),
    path('products/',views.vegie_list, name='shop'),
    path('bottom/',views.bottom, name='bottom'),
    path('hotpicks/',views.hotpicks , name='hotpicks'),
    path('fruit/', views.fruit_list, name='fruit'),
    path('pulse/', views.pulses, name='pulses'),
    path('pulses/', views.pulse_list, name='pulse_list'),
    path('vegies/', views.vegie_list, name='vegie-list'),

    path('contact/', views.contact_view, name='contact'),

#=========================== Wishlist FUNCTIONALITY ===================================

    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-fruit-to-wishlist/<int:fruit_id>/', views.add_fruit_to_wishlist, name='add_fruit_to_wishlist'),
    path('add-pulse-to-wishlist/<int:pulse_id>/', views.add_pulse_to_wishlist, name='add_pulse_to_wishlist'),
    path('add-vegie-to-wishlist/<int:vegie_id>/', views.add_vegie_to_wishlist, name='add_vegie_to_wishlist'),
    path('remove-from-wishlist/<int:wishlist_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),

#========================== CART FUNCTINALITY ===========================================
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/<str:product_type>/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear-cart/', views.clear_cart, name='clear_cart'),
    path('increase-quantity/<int:cart_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease-quantity/<int:cart_id>/', views.decrease_quantity, name='decrease_quantity'),

#============================= Checkout ==================================================

    path('checkout/', views.checkout_view, name='checkout_view'),
    path('order_success/', views.order_success, name='order_success'),
    path('track-order/', views.track_order, name='track_order'),

#================================= User DashBoard ===========================================
    path('admin/', admin.site.urls),  # Default Django Admin
    path('admin-panel/', include('myApp.admin_urls')),  # Custom Admin Panel

    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my-orders/', views.my_orders, name='my_orders'),  
    path('login/', auth_views.LoginView.as_view(template_name='admin_panel/login.html'), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('edit-account/', views.edit_account, name='edit_account'),
    
    path('myfarm/', views.myfarm_list, name='myfarm_list'),

#=========================== COUPEN SYSTEM ================================================

    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('coupons/', views.coupon_list, name='coupon_list'),
    path('admin-panel/coupons/add/', views.add_coupon, name='add_coupon'),
    path('admin-panel/coupons/edit/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('admin-panel/acoupons/delete/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),

#=================== FARM MANAGEMENT =============================================

   path('myfarm/', views.myfarm_list, name='myfarm_list'),
   path('farmer/', views.farmer_list, name='farmer_list'),
   path('producer/', views.producer_list, name='producer_list'),
   path('cow/', views.cow_list, name='cow_list'),

    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)