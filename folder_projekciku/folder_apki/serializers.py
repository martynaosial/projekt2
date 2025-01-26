from rest_framework import serializers
from .models import User, Category, Product, Rental

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'email']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')  # Wyświetla nazwę użytkownika
    owner_role = serializers.ReadOnlyField(source='owner.role')  # Wyświetla rolę użytkownika

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'is_available', 'date_added', 'owner', 'owner_role']

class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = ['id', 'user', 'product', 'status']
