from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  
from .models import User, Category, Product, Rental

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_available', 'date_added']  
    list_filter = ['category', 'is_available', 'date_added']  
    search_fields = ['name', 'description']  
    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description'] 
    
@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'status', 'get_product_category']
    list_filter = ['status', 'product__category']
    search_fields = ['user__username', 'product__name']

    @admin.display(ordering='product__category', description='Category')
    def get_product_category(self, obj):
        return obj.product.category

@admin.register(User)
class CustomUserAdmin(UserAdmin):  # Dziedziczymy po UserAdmin dla dodatkowych funkcji
    fieldsets = UserAdmin.fieldsets + (  # Dodanie pola "role" do edytora użytkownika
        ('Dodatkowe informacje', {'fields': ('role',)}),
    )
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')  # Widoczne kolumny
    list_filter = ('role', 'is_staff', 'is_active')  # Filtrowanie po roli
