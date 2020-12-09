from django.urls import path

from .views import home, Shop, ProductDetail, add_to_cart, remove_from_cart

app_name="shop"

urlpatterns = [
    path('', home.as_view(), name="home"),
    path('list/', Shop.as_view(), name="list"),
    path('detail/<slug>/', ProductDetail.as_view(), name="detail"),
    path('add_to_cart/<slug>/', add_to_cart, name="add_to_cart"),
    path('remove_from_cart/<slug>/', remove_from_cart, name="remove_from_cart"),
]