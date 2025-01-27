from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token
from django.shortcuts import redirect


urlpatterns = [
    path('', lambda request: redirect('product-list')),
    path('admin/', admin.site.urls),
    path('folder_apki/', include('folder_apki.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),

    # Logowanie i rejestracja
    path('login/', auth_views.LoginView.as_view(template_name='folder_apki/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),  # Obsługa logowania i wylogowywania
    path('login/', auth_views.LoginView.as_view(template_name='folder_apki/login.html'), name='login'),
]
