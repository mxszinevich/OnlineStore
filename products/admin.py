from django.contrib import admin
from .models import Score, Order, Product, UserCart

admin.site.register(Score)
admin.site.register(Order)
admin.site.register(Product)
admin.site.register(UserCart)