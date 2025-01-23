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
    path('products/', product_view, name='product-list'),
    path('products/<int:pk>/', product_detail_view, name='product-detail'),

    # Kategorie
    path('categories/<int:category_id>/products/', category_products_view, name='category-products'),

    # Wypożyczenia
    path('rentals/', rental_view, name='rental-list'),
    path('rentals/<int:pk>/', rental_view, name='rental-detail'),

    # Raport miesięczny
    path('rentals/report/monthly/', monthly_rental_report, name='monthly-report'),
]
