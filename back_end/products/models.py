from django.db import models

# Category

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name