from django.urls import path

from basket.views import BasketApiView

app_name = "basket"

urlpatterns = [
    path("basket", BasketApiView.as_view(), name="basket"),
]
