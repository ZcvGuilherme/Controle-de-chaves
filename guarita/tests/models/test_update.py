from django.test import TestCase
from guarita.models import Pessoa, Chave, Historico, ChaveStatus
from django.utils import timezone

#não é prioridade agora
class PessoaUpdateTests(TestCase):
   pass

class ChaveUpdateTests(TestCase):
    pass
class HistoricoUpdateTests(TestCase):
    pass

class ChaveStatusUpdateTests(TestCase):
    def setUp(self):
        self.pessoa1 = Pessoa.objects.create(matricula=1, nome="João", cargo="Professor")
        self.pessoa2 = Pessoa.objects.create(matricula=2, nome="Maria", cargo="Coordenadora")

        self.chave = Chave.registrar_chave(nome="Laboratório de Informática")

    def test_retirar_chave(self):
        
        ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="RETIRADA")

        status = ChaveStatus.objects.get(chave=self.chave)
        self.assertEqual(status.pessoa, self.pessoa1)
        self.assertIsNotNone(status.checkin)
        self.assertFalse(status.status_code)
        self.assertTrue(Historico.objects.filter(acao="RETIRADA", pessoa=self.pessoa1, chave=self.chave).exists())
