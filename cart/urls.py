from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('', cart_detail, name='cart-detail'),
    path('add/<int:product_id>/', cart_add, name='cart-add'),  ## Любой маршрут должна обрабатывать функция (А любая функция должна что-то возвращать)
    path('remove/<int:product_id>/',cart_remove, name='cart-remove'),
]
