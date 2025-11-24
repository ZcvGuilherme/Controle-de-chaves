from django.shortcuts import render
from .models import Chave, ChaveStatus

def chaves(request):
    opcoes_filtro = [
        ('disponivel', 'Disponível'),
        ('indisponivel', 'Indisponível'),
    ]
    return render(request, 'chaves.html', {'opcoes_filtro': opcoes_filtro})

def registrar_chave(request):
    return render(request, 'registrar_chave.html')

def devolver_chave(request):
    return render(request, 'devolver_chave.html')

def status_chave(request):
    return render(request, 'status_chaves.html')

def teste_status(request):
    chaves_status = ChaveStatus.objects.select_related('chave', 'pessoa').all().order_by('chave__id')
    return render(request, 'teste_status.html', {'chaves_status': chaves_status})
