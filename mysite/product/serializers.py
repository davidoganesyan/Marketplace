from rest_framework import serializers

from .models import (CategoryImage, Category, Tag, Reviews, ProductImage, Product, SalesProduct,
                     )


class CategoryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryImage
        fields = ("src", "alt")


class SubCategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()

    class Meta:
        model = Category
        fields = ('id', 'title', 'image')


class CategorySerializer(serializers.ModelSerializer):
    image = CategoryImageSerializer()
    subcategories = serializers.SerializerMethodField("get_subcategories")

    def get_subcategories(self, obj):
        subcategories = obj.subcategories.all()
        return SubCategorySerializer(subcategories, many=True).data

    class Meta:
        model = Category
        fields = ('id', 'title', 'image', 'subcategories')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("name",)


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField("get_author")
    date = serializers.SerializerMethodField("get_date")

    def get_author(self, obj):
        return obj.author.username

    def get_date(self, obj):
        return obj.date.strftime("%Y-%m-%d %H:%M")

    class Meta:
        model = Reviews
        fields = ("author", "email", "text", "rate", "date")


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ("src", "alt")


class ProductSerializerShort(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription', 'freeDelivery',
            'images', 'tags', 'reviews', 'rating',
        )


class ProductSerializerFull(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewsSerializer(many=True)
    specifications = serializers.SerializerMethodField("get_specifications")

    def get_specifications(self, obj):
        if obj.specifications is None:
            return [{"name": "None", "value": "None"}]
        return [{"name": obj.specifications.name, "value": obj.specifications.value}]

    class Meta:
        model = Product
        fields = (
            'id', 'category', 'price', 'count', 'date', 'title', 'description', 'fullDescription', 'freeDelivery',
            'images', 'tags', 'reviews', 'specifications', 'rating',
        )


class SalesSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField("get_price")
    title = serializers.SerializerMethodField("get_title")
    dateFrom = serializers.SerializerMethodField("get_dateFrom")
    dateTo = serializers.SerializerMethodField("get_dateTo")
    images = serializers.SerializerMethodField("get_images")

    def get_images(self, obj):
        qs = ProductImage.objects.filter(product=obj.product)
        images = list({"src": i.src.url, "alt": i.alt} for i in qs)
        return images

    def get_dateTo(self, obj):
        return obj.dateTo.strftime("%m-%d")

    def get_dateFrom(self, obj):
        return obj.dateFrom.strftime("%m-%d")

    def get_price(self, obj):
        return obj.product.price

    def get_title(self, obj):
        return obj.product.title

    class Meta:
        model = SalesProduct
        fields = ("id", "price", "salePrice", "dateFrom", "dateTo", "title", "images")


class CatalogSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)
    tags = TagSerializer(many=True)
    reviews = ReviewsSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'category',
            'price',
            'count',
            'date',
            'title',
            'description',
            'freeDelivery',
            'images',
            'tags',
            'reviews',
            'rating',
        )
