from django.urls import path
from .views import cart_root, cart_add, cart_decrease, cart_remove, cart_clear_all, my_orders


urlpatterns = [
    path("cart", cart_root, name="cart-root"),  # GET and DELETE
    path("cart/add", cart_add, name="cart-add"),
    path("cart/decrease", cart_decrease, name="cart-decrease"),
    path("cart/<id>", cart_remove, name="cart-remove"),
    path("cart/clear-all", cart_clear_all, name="cart-clear-all"),
    path("orders/my", my_orders, name="orders-my"),
]


