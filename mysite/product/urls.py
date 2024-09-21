from django.urls import path

from .views import (CategoryApiView, TagApiView, ProductApiView, ReviewCreateApiView, BannerApiView,
                    LimitedProductApiView, PopularProductApiView, SalesApiView,CatalogApiView)

app_name = "product"

urlpatterns = [
    path("categories/", CategoryApiView.as_view(), name="category"),
    path("tags/", TagApiView.as_view(), name="tag"),
    path("sales/", SalesApiView.as_view(), name="sales"),
    path("catalog/", CatalogApiView.as_view(), name="sales"),
    path("banners/", BannerApiView.as_view(), name="banner"),
    path('product/<int:pk>', ProductApiView.as_view(), name='product'),
    path('product/<int:pk>/reviews', ReviewCreateApiView.as_view(), name='reviews'),
    path('products/limited', LimitedProductApiView.as_view(), name='product_limited'),
    path('products/popular', PopularProductApiView.as_view(), name='product_limited'),
]
