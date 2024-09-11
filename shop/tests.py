from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Product

class EcommerceAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.login(username='testuser', password='testpass')
        self.product = Product.objects.create(name="Test Product", description="Test Description", price=100, quantity_in_stock=10)

    def test_product_list(self):
        response = self.client.get(reverse('product-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_creation(self):
        data = {
            'products': [self.product.id],
        }
        response = self.client.post(reverse('order-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
