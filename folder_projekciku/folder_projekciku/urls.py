from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('folder_apki.urls')),  # Import ścieżek z aplikacji
]