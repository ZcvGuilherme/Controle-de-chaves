
from django.shortcuts import render
from .models import Chave, ChaveStatus
from django.contrib.auth.decorators import login_required

@login_required
def status_chave(request):
    return render(request, 'status_chaves.html')

def teste_status(request):
    chaves_status = ChaveStatus.objects.select_related('chave', 'pessoa').all().order_by('chave__id')
    return render(request, 'teste_status.html', {'chaves_status': chaves_status})
