from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.

class CartUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  ## У одно пользователя не может быть несколько карзин

    def __str__(self) -> str:
        return self.user.username

class CartItem(models.Model):  ## Модель позиции в корзине
    cart = models.ForeignKey(CartUser, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey(Products, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField()


    def __str__(self) -> str:
        return " ".join([self.cart.user.username, self.product.name])
