from django.urls import path
from .views import (
    product_view,
    product_detail_view,
    category_products_view,
    monthly_rental_report,
    rental_view,
)

urlpatterns = [
    # Produkty
    path('api/products/', product_view, name='product-list'),
    path('api/products/<int:pk>/', product_detail_view, name='product-detail'),

    # Kategorie
    path('api/categories/<int:category_id>/products/', category_products_view, name='category-products'),

    # Wypożyczenia
    path('api/rentals/', rental_view, name='rental-list'),
    path('api/rentals/<int:pk>/', rental_view, name='rental-detail'),

    # Raport miesięczny
    path('api/rentals/report/monthly/', monthly_rental_report, name='monthly-report'),
    ]