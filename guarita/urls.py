from django.urls import path
from . import views

urlpatterns = [
    path('', views.chaves, name='chaves'),
    path('registrar/', views.registrar_chave, name='registrar_chave'),
    path('devolver/', views.devolver_chave, name='devolver_chave'),
    path('status/', views.status_chave, name='status_chave'),
    path('teste_status/', views.teste_status, name='teste_status'),
]