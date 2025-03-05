from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # Главная страница — список товаров
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),  # Новый маршрут для корзины
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),  # Новый маршрут оформления заказа
]

