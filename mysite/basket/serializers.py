from collections import OrderedDict
from rest_framework import serializers

from .models import BasketItems
from product.serializers import ProductSerializerShort


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializerShort()

    class Meta:
        model = BasketItems
        fields = ("product", "count")

    def to_representation(self, instance: BasketItems) -> OrderedDict:
        data = super().to_representation(instance)["product"]
        data["count"] = super().to_representation(instance)["count"]
        return data
