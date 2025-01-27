from django.urls import path
from . import views
from .views import register_view
from .views import (
    product_view,
    product_detail_view,
    category_products_view,
    monthly_rental_report,
    rental_view,
    product_search,
    delete_product_admin 
)


urlpatterns = [
    # API JSON
    path('products/', views.product_view, name='product-list'),
    path('products/<int:pk>/', views.product_detail_view, name='product-detail'),
    path('categories/<int:category_id>/products/', views.category_products_view, name='category-products'),
    path('rentals/', views.rental_view, name='rental-list'),
    path('rentals/<int:pk>/', views.rental_view, name='rental-detail'),
    path('rentals/report/monthly/', views.monthly_rental_report, name='monthly-report'),
    path('products/search/<str:query>/', views.product_search, name='product-search'),
    path('products/delete/<int:pk>/', views.delete_product_admin, name='delete-product-admin'),
    path('register/', register_view, name='register'),  # Ścieżka do rejestracji


    # HTML
    path('welcome/', views.welcome_view, name='welcome'),
    path('products_html/', views.product_list_html, name='product-list-html'),
    path('products_html/<int:id>/', views.product_detail_html, name='product-detail-html'),
]