from django.contrib import admin
from .models import Chave, ChaveStatus, Historico, Pessoa

@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'itemBusca')

@admin.register(ChaveStatus)
class ChaveStatus(admin.ModelAdmin):
    list_display = ('chave', 'pessoa', 'status_code', 'checkin')

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id_historico','chave', 'pessoa', 'horario')

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('matricula','itemBusca', 'nome', 'cargo')

