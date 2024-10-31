from django.contrib.auth.models import User
from django.db import models

from product.models import Product


class Order(models.Model):
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    deliveryChoices = [
        ("free", "Free"),
        ("express", "Express"),
        ("standard", "Standard"),
    ]
    paymentChoices = [
        ("online", "Online"),
        ("cash", "payment upon receipt"),
    ]
    statusChoices = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    deliveryType = models.CharField(
        max_length=10, choices=deliveryChoices, default="standard"
    )
    paymentType = models.CharField(
        max_length=10, choices=paymentChoices, default="online"
    )
    totalCost = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=statusChoices, default="pending")
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    products = models.ManyToManyField(Product, related_name="ordered")

    def __str__(self):
        return f"User: {self.user.username},Order ID: {self.pk}"
