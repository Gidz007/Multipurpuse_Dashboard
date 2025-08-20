from django.db import models
from datetime import datetime

# Create your models here.


# The register user class.
class RegisterUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Handling the hashing later on.

    def __str__(self):
        return self.username


# Tracking login activity.
class LoginActivity(models.Model):
    username = models.CharField(max_length=255)
    login_time = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=255)  # Name of the product.
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price of the product.
    supplier = models.CharField(max_length=255)  # Supplier name.
    image = models.ImageField(upload_to="static/media")  # Product image (needs pillow installed)
    expiry_date = models.DateField()  # Expiry date.
    category = models.CharField(max_length=100)  # Category (eg.food).
    serial_number = models.CharField(max_length=50, unique=True)  # Unique serial number.
    recorded_date = models.DateField(default=datetime.now)

    def __str__(self):
        return self.name
