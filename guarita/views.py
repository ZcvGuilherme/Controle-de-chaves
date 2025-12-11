
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST
from django.shortcuts import render
from .models import Chave, ChaveStatus, Pessoa
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone

def filtrar_e_paginar(request):
    filtro_status = request.GET.get("status")
    itemBusca = request.GET.get("busca")

    if filtro_status == "true":
        filtro_status = True
    elif filtro_status == "false":
        filtro_status = False
    else:
        filtro_status = None

    chaves_status = ChaveStatus.getStatus(
        status_code=filtro_status,
        itemBusca=itemBusca
    )

    paginator = Paginator(chaves_status, 5)
    page_number = request.GET.get('page')
    return paginator.get_page(page_number)



@never_cache # Evita cache para garantir que as informações estejam sempre atualizadas
@login_required # Garante que apenas usuários autenticados possam acessar a view
def status_chave(request):
    
    page_obj = filtrar_e_paginar(request)
    hora_atual = timezone.now()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        html = render_to_string(
            'componentes/lista_chaves.html',
            {
                'page_obj': page_obj,
                'hora_atual': hora_atual
                },
            request=request
        )
        return JsonResponse({'html': html})
    
    return render(request, 'status_chaves.html', {'page_obj': page_obj, 'hora_atual':hora_atual})


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
            pessoa = Pessoa.objects.get(matricula=pessoa_id)
        except Pessoa.DoesNotExist:
            return JsonResponse({"erro": "Pessoa não encontrada"}, status=400)
    

    
    ChaveStatus.update(acao=acao,chave=chave,pessoa=pessoa)

    return JsonResponse({"sucesso": True})