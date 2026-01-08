from django.core.management.base import BaseCommand
from guarita.services.backup import backup

class Command(BaseCommand):
    help = "Gera relatório Excel do histórico de chaves"

    def handle(self, *args, **options):
        try:
            backup()
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao gerar backup: {e}"))
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                f"Backup gerado com sucesso!"
            )
        )