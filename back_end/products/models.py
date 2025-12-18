from django.db import models

# Category

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
class Product(models.Model):
    WEIGHT_UNIT_CHOICES = [
        ('g', 'Gram'),
        ('kg', 'Kilogram'),
    ]
    
    weight_value = models.DecimalField(max_digits=5, decimal_places=2)  # 1.5, 5, 10
    weight_unit = models.CharField(max_length=2, choices=WEIGHT_UNIT_CHOICES, default='kg')

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name