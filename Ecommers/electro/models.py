from django.db import models
from django.contrib.auth.models import User



class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self) -> str:
        return f'{self.name}'

class Brand(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, related_name='brands', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.name}'



class Model(models.Model):
    name = models.CharField(max_length=32)
    brand = models.ForeignKey(Brand,related_name='models', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f'{self.name}'



class SubCategory(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.name}'
    

class Product(models.Model):
    name = models.ForeignKey(Brand, on_delete=models.CASCADE)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subcategory = models.ForeignKey(SubCategory, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='media/%Y/%m/%d', blank=True)
    description = models.TextField()
    favorites = models.ManyToManyField(User, related_name='favorites_ads',blank=True)
    
    
    def __str__(self) -> str:
        return f'{self.pk}. {self.name} {self.model}'


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField( blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def get_cart_total(self):
        return sum(item.get_total_price() for item in self.items.all())   
    
    
class Order(models.Model):
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(blank=True, null=True)
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def __str__(self):
        return f"Order {self.id} by {self.customer.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_cost(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    


