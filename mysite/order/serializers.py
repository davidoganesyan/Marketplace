import datetime
from collections import OrderedDict

from rest_framework import serializers

from product.serializers import ProductSerializerShort
from basket.models import Basket, BasketItems
from myauth.models import Profile
from product.models import Product, SalesProduct
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializerShort(many=True)
    fullName = serializers.SerializerMethodField("get_full_name")
    email = serializers.SerializerMethodField("get_email")
    phone = serializers.SerializerMethodField("get_phone")
    createdAt = serializers.SerializerMethodField("get_created_at")
    totalCost = serializers.SerializerMethodField("get_total_cost")

    def get_full_name(self, obj: Order):
        return Profile.objects.get(user=obj.user_id).fullName

    def get_email(self, obj: Order):
        return Profile.objects.get(user=obj.user_id).email

    def get_phone(self, obj: Order):
        return Profile.objects.get(user=obj.user_id).phone

    def get_created_at(self, obj: Order):
        return datetime.datetime.fromisoformat(str(obj.createdAt)).strftime(
            "%Y-%m-%d %H:%M"
        )

    def get_total_cost(self, obj: Order):
        user_cart = Basket.objects.get(user=obj.user)
        items_cart = BasketItems.objects.filter(cart=user_cart, is_paid=0).values(
            "product", "count"
        )
        total = 0
        for item in items_cart:
            if SalesProduct.active_objects.filter(product_id=item["product"]):
                total += (
                    SalesProduct.active_objects.get(
                        product_id=item["product"]
                    ).salePrice
                    * item["count"]
                )
            else:
                total += (
                    Product.active_objects.get(id=item["product"]).price * item["count"]
                )
        return total

    class Meta:
        model = Order
        fields = (
            "id",
            "createdAt",
            "fullName",
            "email",
            "phone",
            "deliveryType",
            "paymentType",
            "totalCost",
            "status",
            "city",
            "address",
            "products",
        )

    def to_representation(self, instance: Order) -> OrderedDict:
        data = super().to_representation(instance)
        user_cart = Basket.objects.get(user=instance.user)
        if instance.status == "paid":
            items_cart = BasketItems.objects.filter(
                cart=user_cart, is_paid=1, order_id=instance.id
            ).values("product", "count")
        else:
            items_cart = BasketItems.objects.filter(cart=user_cart, is_paid=0).values(
                "product", "count"
            )

        for product in data["products"]:
            product["count"] = sum(
                [
                    item["count"]
                    for item in items_cart
                    if item["product"] == product["id"]
                ]
            )
        return data


class OrderHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"

    def to_representation(self, instance: Order, **kwargs) -> OrderedDict:
        data = super().to_representation(instance)
        data["createdAt"] = datetime.datetime.fromisoformat(data["createdAt"]).strftime(
            "%Y-%m-%d %H:%M"
        )
        return data
