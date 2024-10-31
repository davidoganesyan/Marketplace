from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE

from order.models import Order
from product.models import Product


class Basket(models.Model):
    class Meta:
        verbose_name = "Basket"
        verbose_name_plural = "Baskets"

    user = models.OneToOneField(User, on_delete=CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Basket"


class BasketItems(models.Model):
    class Meta:
        verbose_name = "Basket Item"
        verbose_name_plural = "Basket Items"

    cart = models.ForeignKey(Basket, on_delete=CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=CASCADE)
    count = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    order = models.ForeignKey(
        Order, on_delete=CASCADE, null=True, blank=True, related_name="order"
    )

    def __str__(self):
        return f"Basket items for cart {self.cart}"
