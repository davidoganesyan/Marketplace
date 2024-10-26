import random
from datetime import datetime
from urllib.request import Request

from django.db.models import Avg
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from myauth.models import Profile
from .models import Category, Tag, Product, Review, SalesProduct
from .serializers import (CategorySerializer, TagSerializer, ProductSerializerShort, ReviewSerializer, SalesSerializer,
                          CatalogSerializer, ProductSerializerFull)


class CategoryApiView(ListAPIView):
    queryset = Category.objects.filter(parent__isnull=True)
    serializer_class = CategorySerializer


class TagApiView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class ProductApiView(RetrieveAPIView):
    queryset = Product.active_objects.all()
    serializer_class = ProductSerializerFull


def rating_reviews_count_update(product_id):
    ave_rating = Review.objects.filter(product_id=product_id.id).aggregate(Avg('rate')).get("rate__avg")
    reviews_count = Product.objects.filter(pk=product_id.id).values('reviews_count')[0].get('reviews_count')
    Product.objects.filter(pk=product_id.id).update(reviews_count=reviews_count + 1, rating=ave_rating)


class ReviewCreateApiView(APIView):
    def post(self, request: Request, **kwargs) -> Response:
        text = request.data["text"]
        rate = request.data["rate"]
        product_id = Product.active_objects.get(id=kwargs["pk"])
        email = Profile.objects.get(id=request.user.id).email
        data = Review.objects.create(product=product_id, author=request.user, text=text, rate=rate, email=email)
        serialized = ReviewSerializer(data)

        rating_reviews_count_update(product_id)

        return Response(data=serialized.data, status=200)


class BannerApiView(ListAPIView):
    serializer_class = ProductSerializerShort

    def get_queryset(self):
        queryset = random.sample(list(Product.active_objects.all()), 3)
        return queryset


class LimitedProductApiView(ListAPIView):
    serializer_class = ProductSerializerShort

    def get_queryset(self):
        data = Product.active_objects.filter(limited=True)
        data_len = len(data)

        if data_len <= 3:
            queryset = random.sample(list(data), data_len)
        else:
            queryset = random.sample(list(data), 2)
        return queryset


class PopularProductApiView(ListAPIView):
    serializer_class = ProductSerializerShort
    queryset = Product.active_objects.order_by('-rating')[:3]


class CustomPagination(PageNumberPagination):
    page_size = 3
    page_query_param = "currentPage"

    def get_paginated_response(self, data):
        return Response({
            "items": data,
            "currentPage": self.get_page_number(self.request, self.page_size),
            "lastPage": self.page.paginator.num_pages,
        })


class SalesApiView(ListAPIView):
    serializer_class = SalesSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        data = SalesProduct.active_objects.prefetch_related("product").order_by("-id")

        for product in data:
            current_time = datetime.now().timestamp() + 60 * 60 * 3
            if current_time > product.dateTo.timestamp():
                product.is_expires = 1
                product.save()
        return data


class CatalogApiView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = CatalogSerializer

    def get_queryset(self):
        sort = self.request.query_params.get("sort")
        sort_type = self.request.query_params.get("sortType")
        filter_params = self.request.GET
        products = Product.active_objects.all()

        name = filter_params.get('filter[name]')
        if name:
            products = products.filter(title=name)

        min_price = filter_params.get('filter[minPrice]')
        if min_price:
            products = products.filter(price__gte=min_price)

        max_price = filter_params.get('filter[maxPrice]')
        if max_price:
            products = products.filter(price__lte=max_price)

        free_delivery = filter_params.get('filter[freeDelivery]') == 'true'
        if free_delivery:
            products = products.filter(freeDelivery=free_delivery)

        available = filter_params.get('filter[available]')
        if available is not None:
            products = products.filter(amount__gt=0)

        category = filter_params.get('category')
        if category is not None:
            products = products.filter(category=category)

        if sort_type == "inc":
            products = products.order_by(f"-{sort}")
        else:
            products = products.order_by(sort)

        tags = self.request.query_params.getlist("tags[]")
        if tags:
            products = products.filter(tags__in=tags)

        return products
