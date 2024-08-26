from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Product, Order, OrderItem, Brand, Category, Model, SubCategory

class AddToCartViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Category 1')
        self.brand = Brand.objects.create(name='Brand 1', category=self.category)
        self.subcategory = SubCategory.objects.create(name='SubCategory 1', category=self.category)
        self.model = Model.objects.create(name='Model 1', brand=self.brand)
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x00\x00\x00\x00',
            content_type='image/jpeg'
        )
        self.product = Product.objects.create(
            name=self.brand,
            model=self.model,
            price=100.00,
            sale_price=80.00,
            on_sale=True,
            subcategory=self.subcategory,
            stock=10,
            available=True,
            description='Product description',
            image=image_file 
        )

    def test_add_to_cart_new_item(self):
        """Test adding a new product to the cart."""
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        order = Order.objects.get(customer=self.user, paid=False)
        self.assertEqual(order.items.count(), 1)
        order_item = OrderItem.objects.get(order=order, product=self.product)
        
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price, self.product.price)
        self.assertRedirects(response, reverse('home'))

    def test_add_to_cart_existing_item(self):
        """Test updating quantity of an existing product in the cart."""
        self.client.post(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        order = Order.objects.get(customer=self.user, paid=False)
        order_item = OrderItem.objects.get(order=order, product=self.product)
        
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, self.product.price)
        self.assertRedirects(response, reverse('home'))

    def test_add_to_cart_exceed_stock(self):
        """Test handling when trying to add more items than in stock."""
        self.product.stock = 1
        self.product.save()

        self.client.post(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.post(reverse('add_to_cart', args=[self.product.id]))
        order = Order.objects.get(customer=self.user, paid=False)
        order_item = OrderItem.objects.get(order=order, product=self.product)
        
        self.assertEqual(order_item.quantity, 1)
        self.assertRedirects(response, reverse('home'))
