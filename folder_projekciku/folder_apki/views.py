from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.db.models import Count
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import datetime

from .models import Product, Rental, Category
from .serializers import ProductSerializer, RentalSerializer, CategorySerializer

# ====================
# Widoki HTML
# ====================
def product_detail_html(request, id):
    """
    Wyświetla szczegóły produktu w formacie HTML.
    """
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return HttpResponse('Produkt nie istnieje', status=404)
    
    return render(request, 'folder_apki/product_detail.html', {'product': product})


def product_list_html(request):
    """
    Wyświetla listę produktów w formacie HTML.
    - Admin widzi wszystkie produkty.
    - Zwykły użytkownik widzi tylko swoje produkty.
    """
    if request.user.is_staff:
        # Admin widzi wszystkie produkty
        products = Product.objects.filter(is_available=True)
    else:
        # Zwykły użytkownik widzi tylko swoje produkty
        products = Product.objects.filter(owner=request.user, is_available=True)
    
    return render(request, 'folder_apki/product_list.html', {'products': products})


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


def register_view(request):
    """
    Widok obsługujący rejestrację użytkowników.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Tworzy nowego użytkownika
            messages.success(request, 'Konto zostało utworzone! Możesz się teraz zalogować.')
            return redirect('login')  # Przekierowanie na stronę logowania
    else:
        form = UserCreationForm()
    
    return render(request, 'folder_apki/register.html', {'form': form})


# ====================
# Widoki API (JSON)
# ====================
@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def product_view(request):
    """
    Wyświetla listę produktów.
    - Admin widzi wszystkie produkty.
    - Zwykły użytkownik widzi tylko swoje produkty.
    """
    if request.user.is_staff:
        products = Product.objects.filter(is_available=True)
    else:
        products = Product.objects.filter(owner=request.user, is_available=True)

    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def product_detail_view(request, pk):
    """
    Wyświetla szczegóły produktu.
    - Admin widzi wszystkie produkty.
    - Zwykły użytkownik widzi tylko swoje produkty.
    """
    try:
        if request.user.is_staff:
            product = Product.objects.get(pk=pk)
        else:
            product = Product.objects.get(pk=pk, owner=request.user)
    except Product.DoesNotExist:
        return Response({'error': 'Produkt nie istnieje lub nie należy do użytkownika.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def product_search(request, query):
    """
    Wyszukuje produkty na podstawie fragmentu nazwy.
    - Admin widzi wszystkie produkty pasujące do zapytania.
    - Zwykły użytkownik widzi tylko swoje produkty pasujące do zapytania.
    """
    if request.user.is_staff:
        # Admin widzi wszystkie produkty pasujące do zapytania
        products = Product.objects.filter(name__icontains=query)
    else:
        # Zwykły użytkownik widzi tylko swoje produkty pasujące do zapytania
        products = Product.objects.filter(owner=request.user, name__icontains=query)
    
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def category_products_view(request, category_id):
    """
    Wyświetla produkty z wybranej kategorii przypisane do zalogowanego użytkownika.
    """
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        return Response({'error': 'Kategoria nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

    products = Product.objects.filter(category=category, owner=request.user, is_available=True)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
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
@authentication_classes([TokenAuthentication, SessionAuthentication])
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


@api_view(['DELETE'])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAdminUser])
def delete_product_admin(request, pk):
    """
    Usuwa dowolny produkt na podstawie jego ID.
    Endpoint dostępny tylko dla adminów.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Produkt nie istnieje.'}, status=status.HTTP_404_NOT_FOUND)

    product.delete()
    return Response({'message': f'Produkt o ID {pk} został usunięty.'}, status=status.HTTP_204_NO_CONTENT)
