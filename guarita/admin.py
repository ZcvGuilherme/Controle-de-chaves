from django.contrib import admin
from .models import Chave, ChaveStatus, Historico, Pessoa

@admin.register(Chave)
class ChaveAdmin(admin.ModelAdmin):
    exclude = ('itemBusca',)
    list_display = ('id','nome', 'itemBusca')
    list_display_links = ('id', 'nome')
@admin.register(ChaveStatus)
class ChaveStatusAdmin(admin.ModelAdmin):
    list_display = ('chave', 'pessoa', 'status_code', 'checkin')
    list_display_links = ('chave', 'pessoa')

@admin.register(Historico)
class HistoricoAdmin(admin.ModelAdmin):
    list_display = ('id_historico','acao','chave', 'pessoa', 'horario')
    list_display_links = ('id_historico', 'chave')
@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    exclude = ('user',)
    list_display = ('matricula', 'nome', 'user')
    list_display_links = ('matricula',)  # matricula é o link clicável
