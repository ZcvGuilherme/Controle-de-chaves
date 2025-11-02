
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('guarita.urls')),  # Inclui URLs do app guarita
    
]
