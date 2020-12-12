from django.urls import path

from .views import home, ProductDetail, add_to_cart, remove_from_cart, OrderSummary, remove_single_item_from_cart, CheckOut

app_name="shop"

urlpatterns = [
    path('', home.as_view(), name="home"),

    path('order_summary/', OrderSummary.as_view(), name='order_summary'),

    path('checkout/', CheckOut.as_view(), name="checkout" ),

    path('detail/<slug>/', ProductDetail.as_view(), name="detail"),
    path('add_to_cart/<slug>/', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<slug>/', remove_from_cart, name="remove_from_cart"),
    path('remove_single/<slug>/', remove_single_item_from_cart, name="remove_single")
]