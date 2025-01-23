from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import Product, Rental, Category
from .serializers import ProductSerializer, RentalSerializer, CategorySerializer
from django.db.models import Count
from django.utils.timezone import now


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_view(request):
    """
    Obsługuje operacje listy produktów oraz tworzenia nowych.
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
    Obsługuje szczegóły produktu, aktualizację oraz usuwanie.
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
    Obsługuje wypożyczenia.
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
