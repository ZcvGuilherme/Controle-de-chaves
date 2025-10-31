from django.shortcuts import render

def chaves(request):
    return render(request, 'chaves.html')

def registrar_chave(request):
    return render(request, 'registrar_chave.html')

def devolver_chave(request):
    return render(request, 'devolver_chave.html')