from django.contrib import admin
from .models import Chave, ChaveStatus, Historico, Pessoa, Restricao
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ChaveResource(resources.ModelResource):
    class Meta:
        model = Chave

class PessoaResource(resources.ModelResource):
    class Meta:
        model = Pessoa
        import_id_fields = ('matricula',)


@admin.register(Chave)
class ChaveAdmin(ImportExportModelAdmin):
    resource_class = ChaveResource
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
class PessoaAdmin(ImportExportModelAdmin):
    resource_class = PessoaResource
    exclude = ('user',)
    list_display = ('matricula', 'nome', 'user')
    list_display_links = ('matricula',)  # matricula é o link clicável


@admin.register(Restricao)
class RestricaoAdmin(admin.ModelAdmin):
    list_display = ("pessoa", "chave")
    list_filter = ("pessoa", "chave")
    search_fields = ("pessoa__nome", "chave__nome")