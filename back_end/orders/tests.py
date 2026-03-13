from django.test import TestCase
from django.utils import timezone
from decimal import Decimal

from accounts.models import Register
from products.models import Product
from .models import Address, Order, OrderItem

# Create your tests here.

class AddressModelTest(TestCase):

    def setUp(self):
        self.user = Register.objects.create_user(
            email="testuser@example.com",
            password="testpass123"
        )

        self.address = Address.objects.create(
            user=self.user,
            full_name="Prince Biju",
            mobile="9876543210",
            street="MG Road",
            city="Bangalore",
            state="Karnataka",
            zip_code="560001",
            country="India"
        )

    def test_address_creation(self):
        self.assertEqual(self.address.user, self.user)
        self.assertEqual(self.address.city, "Bangalore")

    def test_address_str_method(self):
        self.assertEqual(
            str(self.address),
            "Prince Biju - Bangalore"
        )
