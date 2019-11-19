
from django.urls import path
from . import views

urlpatterns = [
    path('', views.cover_view, name='cover_view'),
    path('shop/', views.shop_view, name='shop_view'),
    path('shop/<str:category_slug>/', views.shop_view, name='category_detail'),
    path('shop/product/<str:product_slug>/', views.product_view, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add_to_cart/', views.add_to_cart_view, name='add_to_cart'),
    path('remove_from_cart/', views.remove_from_cart_view, name='remove_from_cart'),
    path('change_item_qty/', views.change_item_qty, name='change_item_qty'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/', views.order_crate_view, name='create_order'),
    path('thank_you/', views.thank_you_view, name='thank_you'),
    path('make_order/', views.make_order_view, name='make_order'),
    path('account/orders', views.accoun_orders_view, name='account_orders'),
    path('account/registration', views.registration_view, name='registration'),
    path('logout', views.logout_view, name='logout'),


]



