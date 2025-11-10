from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.text import slugify
from products.models import Product
# ✅ Custom User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    # Fix Django warnings
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True
    )


# ✅ Product Model
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)  # auto generate if blank
    category = models.CharField(max_length=50)
    weight = models.FloatField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    description = models.TextField()

    # ✅ Image will be stored in /media/products/
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # ✅ Auto-generate slug if empty
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ✅ Order Model
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Product)

    shipping_address = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)
    admin_notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"
