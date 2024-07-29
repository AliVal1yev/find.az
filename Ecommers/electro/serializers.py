from rest_framework import serializers
from .models import Product, Customer, Category, SubCategory, Order




class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fileds = '__all__'
        