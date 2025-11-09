from django.shortcuts import render

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