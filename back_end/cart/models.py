from django.db import models
from accounts.models import Register
from products.models import Product
# from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)