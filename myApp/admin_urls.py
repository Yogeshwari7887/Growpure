from django.urls import path
from .views import admin_dashboard, manage_orders, manage_users , manage_products ,delete_feedback, add_product , edit_product ,manage_feedback, delete_product , delete_user ,add_user, edit_user , edit_order , cancel_order

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('orders/', manage_orders, name='manage_orders'),
    path('users/', manage_users, name='manage_users'),
    path("admin-panel/products/", manage_products, name="manage_products"),
    path("admin-panel/products/add/", add_product, name="add_product"),
    path("edit-product/<str:category>/<int:product_id>/", edit_product, name="edit_product"),
    path("admin-panel/products/delete/<int:product_id>/", delete_product, name="delete_product"),
    path("admin-panel/users/delete/<int:user_id>/", delete_user, name="delete_user"),
    path("admin-panel/users/edit/<int:user_id>/", edit_user, name="edit_user"),
    path("admin-panel/users/add/", add_user, name="add_user"),  
    path("admin-panel/orders/edit/<int:order_id>/", edit_order, name="edit_order"),
    path("admin-panel/orders/cancel/<int:order_id>/", cancel_order, name="cancel_order"),
    path('admin/feedback/', manage_feedback, name="manage_feedback"),
    path('admin/feedback/delete/<int:feedback_id>/', delete_feedback, name="delete_feedback"),
]

