from django.core.management.base import BaseCommand
from guarita.services.historico_service import gerar_dataframe_historico

class Command(BaseCommand):
    help = "Gera relatório Excel do histórico de chaves"

    def handle(self, *args, **options):
        df = gerar_dataframe_historico()

        if df.empty:
            self.stdout.write(
                self.style.WARNING("Nenhum dado encontrado no histórico.")
            )
            return

        nome_arquivo = "relatorio_historico_chaves.xlsx"
        df.to_excel(nome_arquivo, index=False)

        self.stdout.write(
            self.style.SUCCESS(
                f"Relatório gerado com sucesso: {nome_arquivo}"
            )
        )