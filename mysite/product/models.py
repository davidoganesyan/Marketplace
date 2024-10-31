from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


def category_images_directory_path(instance: "Category", filename: str) -> str:
    return f"category/category_{instance.category.pk}/{filename}"


class Category(models.Model):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    title = models.CharField(max_length=50)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="subcategories",
    )

    def __str__(self):
        return f"Category: {self.title}, ID - {self.pk}"


class CategoryImage(models.Model):
    class Meta:
        verbose_name = "Category image"
        verbose_name_plural = "Category images"

    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, related_name="image"
    )
    src = models.ImageField(upload_to=category_images_directory_path)
    alt = models.CharField(max_length=200, null=False, blank=True)

    def __str__(self):
        return f"{self.category}, Url: {self.src}"


class Specifications(models.Model):
    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"

    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __str__(self):
        return f"Specifications: {self.name} - {self.value}"


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    price = models.DecimalField(max_digits=11, decimal_places=2)
    amount = models.IntegerField(default=1)
    ordered_amount = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    fullDescription = models.TextField(max_length=10**4)
    freeDelivery = models.BooleanField(default=False)
    reviews_count = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=3.0)
    limited = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    specifications = models.ForeignKey(
        Specifications,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="specifications",
    )

    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_available=True, is_archived=False)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return f"Product: {self.title}, ID - {self.pk}"


def product_images_directory_path(instance: "Product", filename: str) -> str:
    return f"products/product_{instance.product.pk}/{filename}"


class ProductImage(models.Model):
    class Meta:
        verbose_name = "Product image"
        verbose_name_plural = "Product images"

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    src = models.ImageField(
        upload_to=product_images_directory_path, null=True, blank=True
    )
    alt = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.product}, Url: {self.src.url}"


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=50)
    product = models.ManyToManyField(
        Product,
        blank=True,
        related_name="tags",
    )

    def __str__(self):
        return f"Tag: {self.name}"


class Review(models.Model):
    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    text = models.TextField(max_length=10**4)
    email = models.EmailField(max_length=250)
    rate = models.DecimalField(max_digits=2, decimal_places=1, default=3.0)
    date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews", blank=True, null=True
    )

    def __str__(self):
        return f"{self.product.title}, Author: {self.author}"


class SalesProduct(models.Model):
    class Meta:
        verbose_name = "Sales Product"
        verbose_name_plural = "Sales Products"

    salePrice = models.DecimalField(max_digits=10, decimal_places=2)
    dateFrom = models.DateTimeField()
    dateTo = models.DateTimeField()
    product = models.OneToOneField(Product, on_delete=CASCADE, blank=True, null=True)
    is_expires = models.BooleanField(default=False)

    def expire(self):
        if datetime.now() >= self.dateTo:
            self.is_expires = True

    class ActiveManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(is_expires=False)

    objects = models.Manager()
    active_objects = ActiveManager()

    def __str__(self):
        return f"product {self.product}"
