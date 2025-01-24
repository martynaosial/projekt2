from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Count
import datetime

from .models import Product, Rental, Category
from .serializers import ProductSerializer, RentalSerializer, CategorySerializer


# ====================
# Widoki API (JSON)
# ====================
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_view(request):
    """
    Obsługuje API listy produktów (GET) oraz tworzenie nowych (POST).
    """
    if request.method == 'GET':
        products = Product.objects.filter(is_available=True)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff:  # Sprawdzanie uprawnień admina
            return Response({'error': 'Brak uprawnień'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_detail_view(request, pk):
    """
    Obsługuje API szczegółów produktu, aktualizację oraz usuwanie.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Produkt nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_staff:  # Sprawdzanie uprawnień admina
            return Response({'error': 'Brak uprawnień'}, status=status.HTTP_403_FORBIDDEN)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_staff:  # Sprawdzanie uprawnień admina
            return Response({'error': 'Brak uprawnień'}, status=status.HTTP_403_FORBIDDEN)
        product.delete()
        return Response({'message': 'Produkt został usunięty'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def category_products_view(request, category_id):
    """
    Wyświetla produkty z wybranej kategorii.
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Kategoria nie istnieje'}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(category=category, is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def monthly_rental_report(request):
    """
    Zwraca raport miesięczny wypożyczeń.
    """
    current_month = now().month
    rentals = (
        Rental.objects.filter(start_date__month=current_month)
        .values('start_date__date')
        .annotate(count=Count('id'))
    )
    return Response(rentals)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def rental_view(request, pk=None):
    """
    Obsługuje API wypożyczeń.
    """
    if request.method == 'GET':
        if pk:
            try:
                rental = Rental.objects.get(pk=pk, user=request.user)
            except Rental.DoesNotExist:
                return Response({'error': 'Wypożyczenie nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
            serializer = RentalSerializer(rental)
            return Response(serializer.data)
        else:
            rentals = Rental.objects.filter(user=request.user)
            serializer = RentalSerializer(rentals, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = RentalSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ====================
# Widoki HTML
# ====================
def welcome_view(request):
    """
    Prosty widok pokazujący datę i czas w formacie HTML.
    """
    now = datetime.datetime.now()
    html = f"""
        <html><body>
        Witaj użytkowniku! </br>
        Aktualna data i czas na serwerze: {now}.
        </body></html>"""
    return HttpResponse(html)


def product_list_html(request):
    """
    Wyświetla listę produktów w formacie HTML.
    """
    products = Product.objects.filter(is_available=True)
    return render(request, 'folder_apki/product_list.html', {'products': products})


def product_detail_html(request, id):
    """
    Wyświetla szczegóły produktu w formacie HTML.
    """
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse('Produkt nie istnieje', status=404)
    
    return render(request, 'folder_apki/product_detail.html', {'product': product})
