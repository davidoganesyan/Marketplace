from django.urls import path

from .views import OrderApiView, OrdersDetailApiView, PaymentApiView

app_name = "order"

urlpatterns = [
    path("orders", OrderApiView.as_view(), name="orders"),
    path("order/<int:id>", OrdersDetailApiView.as_view(), name="order"),
    path("payment/<int:id>", PaymentApiView.as_view(), name="payment"),
]
