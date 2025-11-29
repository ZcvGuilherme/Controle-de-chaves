
from django.views.decorators.cache import never_cache
from django.shortcuts import render
from .models import Chave, ChaveStatus
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@never_cache # Evita cache para garantir que as informações estejam sempre atualizadas
@login_required # Garante que apenas usuários autenticados possam acessar a view
def status_chave(request):

    chaves_status = ChaveStatus.getStatus()
    paginator = Paginator(chaves_status, 2) # Mostrar X itens por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'status_chaves.html', {'page_obj': page_obj})


