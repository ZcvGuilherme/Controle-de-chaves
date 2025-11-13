from django.contrib import admin
from .models import Chave, ChaveStatus, Historico, Pessoa

@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
    list_display = ('id','nome', 'itemBusca')
    list_display_links = ('id', 'nome')
@admin.register(ChaveStatus)
class ChaveStatus(admin.ModelAdmin):
    list_display = ('chave', 'pessoa', 'status_code', 'checkin')
    list_display_links = ('chave', 'pessoa')
@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id_historico','chave', 'pessoa', 'horario')
    list_display_links = ('id_historico', 'chave')
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display = ('matricula','itemBusca', 'nome', 'cargo')
    list_display_links = ('matricula', 'itemBusca')
