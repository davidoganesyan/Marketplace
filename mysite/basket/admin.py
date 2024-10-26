from django.contrib import admin

from .models import Basket, BasketItems

admin.site.register(BasketItems)
admin.site.register(Basket)
