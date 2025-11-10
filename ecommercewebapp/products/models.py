
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50)
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/')
    description = models.TextField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
# Create your models here.
