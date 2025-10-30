from datetime import datetime
from django.test import TestCase
from guarita.models import Pessoa, Chave, Historico, ChaveStatus
from django.db import IntegrityError
class PessoaInsertModelTest(TestCase):
    def test_registrar_pessoa(self):
        Pessoa.registrar_pessoa(matricula= 1, nome= "João", cargo= "Professor")
        
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertEqual(Pessoa.nome, "João")
        self.assertEqual(Pessoa.cargo, "Professor")
    

    def test_duplicata_de_pessoa(self):
        Pessoa.registrar_pessoa(matricula= 1, nome= "João", cargo= "Professor")

        with self.assertRaises(IntegrityError):
            Pessoa.registrar_pessoa(1, "Carlos", "Técnico")


class ChaveInsertModelTest(TestCase):
    def test_registrar_pessoa(self):
        Chave.registrar_chave(nome= "Laboratório de Informática")

        self.assertEqual(Chave.objects.count(), 1)
        self.assertEqual(Chave.nome, "Laboratório de Informática")

class HistoricoInsertModelTest(TestCase):
    def setUp(self):
        self.pessoa = Pessoa.objects.create(
            matricula = 1,
            nome="João",
            cargo="Professor"
        )
        self.chave = Chave.objects.create(
            id=1,
            nome="Laboratório de Informática"
        )

    def test_registrar_acesso_historico(self):
        data_atual = datetime.now()
        id_historico= int(data_atual.strftime("%Y%m%d%H%M%S"))

        Historico.registrar_acesso(
            id_historico=id_historico,
            acao="RETIRADA",
            id_pessoa = self.pessoa,
            id_chave= self.chave,
            horario=data_atual
        )

        self.assertEqual(Historico.objects.count(), 1)
        registro = Historico.get_acess_by_id(id_historico)
        

        self.assertEqual(registro.acao, "RETIRADA")
        self.assertEqual(registro.id_pessoa.nome, "João")
        self.assertEqual(registro.id_chave.nome, "Laboratório de Informática")
        self.assertEqual(registro.horario, data_atual)
    
    def test_historico_com_pessoa_inexistente(self):
        data_atual = datetime.now()
        id_historico = int(data_atual.strftime("%Y%m%d%H%M%S"))

        with self.assertRaises(IntegrityError):
            Historico.registrar_acesso(
                id_historico=id_historico,
                acao="RETIRADA",
                id_pessoa=999,
                id_chave=self.chave,
                horario=data_atual
            )
    def test_historico_com_chave_inexistente(self):
        data_atual = datetime.now()
        id_historico = int(data_atual.strftime("%Y%m%d%H%M%S"))

        with self.assertRaises(IntegrityError):
            Historico.registrar_acesso(
                id_historico=id_historico,
                acao="RETIRADA",
                id_pessoa=self.pessoa,
                id_chave=777,
                horario=data_atual
            )
    
class ChaveStatusInsertModelTest(TestCase):
    def setUp(self):
        self.pessoa = Pessoa.objects.create(
            matricula=1,
            nome="João",
            cargo="Professor"
        )
        self.chave = Chave.objects.create(
            id=1,
            nome="Laboratório de Informática"
        )
    def test_verificar_insert_funciona(self):
        ChaveStatus.criar_status(
            id_chave=self.chave,
            id_pessoa=self.pessoa,
            checkin=datetime.now()
        )
    def test_insert_chave_disponivel(self):
        status = ChaveStatus.criar_status(
            id_chave=self.chave,
            id_pessoa=None,
            checkin=None
        )
        self.assertTrue(status.status_code)
        print(f"Status criado: {status} (esperado: Disponível=True)")

    def test_insert_chave_indisponivel(self):
        status = ChaveStatus.criar_status(
            id_chave=self.chave,
            id_pessoa=self.pessoa,
            checkin=datetime.now()
        )
        self.assertFalse(status.status_code)
        print(f"Status criado: {status} (esperado: Disponível=False)")

    def test_insert_sem_pessoa(self):
        """
        Deve permanecer disponível caso id_pessoa esteja None
        """
        status = ChaveStatus.criar_status(
            id_chave=self.chave,
            id_pessoa=None,
            checkin=datetime.now()
        )
        self.assertTrue(status.status_code)
        print(f"Status criado: {status} (esperado: Disponível=True)")