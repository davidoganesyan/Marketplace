from django.contrib import admin

from .models import Category, CategoryImage, Product, ProductImage, Tag, Specifications, Reviews, SalesProduct

admin.site.register(CategoryImage)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Tag)
admin.site.register(Specifications)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(SalesProduct)
