from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog, name='catalog'),
    path('cart/',views.cart,name="cart"),
    path('cart/remove/',views.removefromcart,name="remove"),
    path('cart/cart/checkout/',views.checkout,name="checkout"),
    path('cart/checkout/',views.checkout,name="checkout"),
    path('cart/cart/checkout/complete/',views.completeOrder,name="complete_order"),
    path('cart/checkout/complete/',views.completeOrder,name="complete_order"),
    path('admin-login/',views.adminLogin,name="admin_login"),
    path('admin-panel/',views.adminDashboard,name="admin"),
]