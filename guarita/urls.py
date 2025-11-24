from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.chaves, name='chaves'),
    path('registrar/', views.registrar_chave, name='registrar_chave'),
    path('devolver/', views.devolver_chave, name='devolver_chave'),
    path('status/', views.status_chave, name='status_chave'),
    path('accounts/', include('django.contrib.auth.urls')),
]

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()