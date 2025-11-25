from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Chave



@login_required
def status_chave(request):
    return render(request, 'status_chaves.html')
