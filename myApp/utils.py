# from django.core.mail import send_mail
# from django.conf import settings

# def send_order_update_email(order):
#     """Sends an email to the customer when the order status is updated."""
#     subject = f"Order #{order.id} Update - {order.status}"
#     message = f"""
#     Dear {order.full_name},

#     Your order status has been updated.

#     Order Details:
#     - Order ID: {order.id}
#     - Total Amount: ₹{order.total_price}
#     - Payment Method: {order.get_payment_method_display()}
#     - Current Status: {order.status}

#     Thank you for shopping with us!

#     Best Regards,  
#     GrowPure Team
#     """

#     send_mail(
#         subject,
#         message,
#         settings.DEFAULT_FROM_EMAIL,
#         [order.email],  # Send email to customer
#         fail_silently=False,
#     )
