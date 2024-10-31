from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from basket.models import BasketItems, Basket
from .models import Order
from .serializers import OrderSerializer, OrderHistorySerializer
from product.models import Product


class OrderApiView(APIView):
    def get(self, request: Request) -> Response:
        user_order = Order.objects.filter(user=request.user)
        serializer = OrderHistorySerializer(user_order, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        user_basket = Basket.objects.get(user=request.user)
        basket_items = BasketItems.objects.filter(cart_id=user_basket, is_paid=0)
        products_list = Product.objects.filter(
            id__in=basket_items.values_list("product", flat=True)
        )
        data = Order.objects.create(user=request.user)
        data.products.set(products_list)
        data.save()
        return Response(data={"orderId": data.id}, status=200)


class OrdersDetailApiView(APIView, IsAuthenticated):
    def get(self, request: Request, **kwargs) -> Response:
        serialized = OrderSerializer(Order.objects.get(id=kwargs["id"]))
        return Response(serialized.data, status=200)

    def post(self, request: Request, **kwargs) -> Response:
        user_basket = Basket.objects.get(user=request.user)
        basket_items = BasketItems.objects.filter(cart_id=user_basket, is_paid=0)
        for item in basket_items:
            item.order_id = kwargs["id"]
            item.save()
        order = Order.objects.get(pk=kwargs["id"])
        order.deliveryType = request.data["deliveryType"]
        order.paymentType = request.data["paymentType"]
        order.totalCost = request.data["totalCost"]
        order.status = "accepted"
        order.city = request.data["city"]
        order.address = request.data["address"]
        order.save()
        return Response({"orderId": order.id})


class PaymentApiView(APIView):
    def post(self, request: Request, **kwargs) -> Response:
        number = request.data["number"]
        name = request.data["name"]
        month = request.data["month"]
        year = request.data["year"]
        code = request.data["code"]

        user_order = Order.objects.get(id=kwargs["id"])
        user_order.status = "paid"
        user_order.save()

        user_basket_items = BasketItems.objects.filter(
            cart_id=request.user.id, is_paid=0
        )
        for item in user_basket_items:
            ordered_product = Product.objects.get(id=item.product_id)
            ordered_product.amount = ordered_product.amount - item.count
            if ordered_product.amount == 0:
                ordered_product.is_available = False
            ordered_product.save()
            item.is_paid = 1
            item.save()
        return Response({number, name, month, year, code}, status=200)
