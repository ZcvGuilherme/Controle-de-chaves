
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import Chave, ChaveStatus, Pessoa
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


@never_cache # Evita cache para garantir que as informações estejam sempre atualizadas
@login_required # Garante que apenas usuários autenticados possam acessar a view
def status_chave(request):

    chaves_status = ChaveStatus.getStatus()
    paginator = Paginator(chaves_status, 2) # Mostrar X itens por página

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'status_chaves.html', {'page_obj': page_obj})


@require_POST
@login_required
def atualizar_status(request):
    chave_id = request.POST.get("chave_id")
    pessoa_id = request.POST.get("pessoa_id")
    acao = request.POST.get("acao")

    chave = Chave.objects.get(id=chave_id)
    pessoa = None
    if pessoa_id:  # só busca se tiver valor
        try:
            pessoa = Pessoa.objects.get(id=pessoa_id)
        except Pessoa.DoesNotExist:
            return JsonResponse({"erro": "Pessoa não encontrada"}, status=400)
        
    ChaveStatus.update(acao=acao,chave=chave,pessoa=pessoa)

    return JsonResponse({"sucesso": True})