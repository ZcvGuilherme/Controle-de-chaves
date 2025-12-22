
import pandas as pd
from guarita.models import Historico
from django.utils.timezone import localtime

def gerar_dataframe_historico():
    queryset = Historico.objects.select_related(
        'pessoa', 'chave'
    ).order_by('-horario')

    dados = []

    for h in queryset:
        horario_local = localtime(h.horario).replace(tzinfo=None)

        dados.append({
            "Pessoa": h.pessoa.nome,
            "Matrícula": h.pessoa.matricula,
            "Chave": h.chave.nome,
            "Ação": h.get_acao_display(),
            "Data": horario_local.strftime("%d/%m/%Y"),
            "Hora": horario_local.strftime("%H:%M:%S"),
            # NÃO coloque Timestamp timezone-aware no Excel
        })

    return pd.DataFrame(dados)
