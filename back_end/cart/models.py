from django.db import models
from accounts.models import User
# from products.models import Product
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f"Cart - {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'