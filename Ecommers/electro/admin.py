from django.contrib import admin
from .models import Product, Category, SubCategory, Customer, Order, OrderItem, Brand, Model



class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'price', 'sale_price', 'on_sale', 'stock', 'available', 'created_at', 'updated_at']
    list_filter = ['on_sale', 'available', 'created_at', 'updated_at']
    search_fields = ['name__name', 'subcategory__name', 'model__name']
    
    
    
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('product', 'quantity', 'price')
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'updated_at', 'paid', 'paid_at']
    list_filter = ['paid', 'created_at', 'updated_at']
    search_fields = ['customer__username', 'customer__email']
    inlines = [OrderItemInline]
    readonly_fields = ('get_total_cost',)
    
    def get_total_cost(self, obj):
        return obj.get_total_cost()
    get_total_cost.short_description = 'Total Cost'

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']
    list_filter = ['order', 'product']
    search_fields = ['order__customer__username', 'product__name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model', 'price', 'sale_price', 'on_sale', 'stock', 'available']
    list_filter = ['on_sale', 'available', 'created_at', 'updated_at']
    search_fields = ['name', 'description', 'subcategory__name', 'model__name']    
    
    
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']

class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name', 'category__name']
    
class ModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand']
    search_fields = ['name', 'brand__name']
        
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Brand)
admin.site.register(Model, ModelAdmin)


