from django.contrib import admin
from .models import Product, Category, SubCategory, Customer, Order, OrderItem, Brand, Model


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Brand)
admin.site.register(Model)


