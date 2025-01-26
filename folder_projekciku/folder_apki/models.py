from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('adminki', 'Administrator'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    
    def save(self, *args, **kwargs):
        # Automatycznie ustawiaj `is_staff` na True, jeśli rola to `adminki`
        if self.role == 'adminki':
            self.is_staff = True  # Użytkownicy z rolą 'adminki' będą mieli dostęp do panelu admina
        else:
            self.is_staff = False  # Zwykli użytkownicy nie mają dostępu do panelu admina
        super().save(*args, **kwargs)  # Zapisz obiekt

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Odniesienie do niestandardowego modelu użytkownika
        on_delete=models.CASCADE
    )
    
    def clean(self):
        if len(self.name) < 3:
            raise ValidationError("Nazwa produktu musi mieć co najmniej 3 znaki.")
        if self.description.strip() == "":
            raise ValidationError("Opis produktu nie może być pusty.")

    def check_availability(self):
        return "Dostępny" if self.is_available else "Niedostępny"

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Rental(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('returned', 'Returned'),
    ]
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(default=now)

    def is_pending(self):
        return self.status == 'pending'

    def __str__(self):
        return f"{self.user.username} rented {self.product.name}"

