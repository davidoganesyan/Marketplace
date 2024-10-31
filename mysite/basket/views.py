from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from .models import Basket, BasketItems
from .serializers import BasketSerializer


class BasketApiView(APIView):
    def get(self, request: Request) -> Response:
        users_basket, _ = Basket.objects.get_or_create(user=request.user)
        serializer = BasketSerializer(users_basket.items.filter(is_paid=0), many=True)
        return Response(serializer.data, status=200)

    def post(self, request: Request) -> Response:
        users_basket, _ = Basket.objects.get_or_create(user=request.user)
        product_id = request.data.get("id")
        count = request.data.get("count", 0)
        product = get_object_or_404(Product, id=product_id)
        if count > product.amount:
            count = product.amount

        basket_item, created = BasketItems.objects.get_or_create(
            cart=users_basket, product=product, is_paid=0
        )

        if basket_item.count < product.amount:
            basket_item.count += int(count)

        basket_item.save()
        serializer = BasketSerializer(users_basket.items.filter(is_paid=0), many=True)
        return Response(serializer.data)

    def delete(self, request: Request) -> Response:
        users_basket = Basket.objects.get(user=request.user.id)
        product_id = request.data.get("id")
        basket_item = get_object_or_404(
            BasketItems, cart=users_basket, product=product_id, is_paid=0
        )
        basket_item.count -= request.data.get("count", 0)
        if basket_item.count > 0:
            basket_item.save()
        else:
            basket_item.delete()
        serializer = BasketSerializer(users_basket.items.filter(is_paid=0), many=True)
        return Response(serializer.data)
