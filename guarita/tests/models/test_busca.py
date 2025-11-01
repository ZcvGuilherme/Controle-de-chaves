from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.test import TestCase
from guarita.models import Pessoa, Chave, Historico, ChaveStatus
from django.db.models.query import QuerySet
from datetime import datetime
class PessoaBuscaTests(TestCase):
    def setUp(self):
        self.pessoa1 = Pessoa.objects.create(
            matricula=1,
            nome="João",
            cargo= "Professor"
        )
        self.pessoa2 = Pessoa.objects.create(
            matricula=2,
            nome="Maria",
            cargo= "Técnico"
        )
        self.pessoa3 = Pessoa.objects.create(
            matricula=3,
            nome="Joana",
            cargo="Bibliotecário"
        )
        self.pessoa4 = Pessoa.objects.create(
            matricula=4,
            nome="Jorge",
            cargo="Professor"
        )

    def test_busca_por_id(self):
        busca = Pessoa.search_by_matricula(self.pessoa1.matricula)

        self.assertIsNotNone(busca)
        self.assertEqual(busca.nome, self.pessoa1.nome)
        self.assertEqual(busca.cargo, self.pessoa1.cargo)

    def test_busca_por_cargo(self):
        busca = Pessoa.search_by_cargo("Professor")

        self.assertIsNotNone(busca)
        self.assertIsInstance(busca, QuerySet)
        self.assertEqual(busca.count(), 2)

        nomes= [p.nome for p in busca]
        self.assertIn("João", nomes)
        self.assertIn("Jorge", nomes)

    def test_busca_parcial(self):
        busca = Pessoa.partial_search(content="Jo")
        nomes = [p.nome for p in busca]
        self.assertCountEqual(nomes, ["João", "Joana", "Jorge"])

    def test_busca_retorno_todas_as_pessoas(self):
        busca = Pessoa.getAll()
        nomes = [p.nome for p in busca]
        self.assertCountEqual(nomes, ["João", "Maria", "Joana", "Jorge"])

class ChaveBuscaTests(TestCase):
    def setUp(self):
        self.chave1 = Chave.objects.create(nome="Laboratório de Informática")
        self.chave2 = Chave.objects.create(nome="Laboratório de Química")
        self.chave3 = Chave.objects.create(nome="Biblioteca")

    def test_busca_por_id(self):
        busca = Chave.search_by_id(self.chave1.id)

        self.assertIsNotNone(busca)
        self.assertEqual(busca.id, self.chave1.id)
        self.assertEqual(busca.nome, self.chave1.nome)
    
    def test_busca_por_nome(self):
        busca = Chave.search_by_nome("Laboratório de Informática")

        self.assertIsInstance(busca, QuerySet)
        self.assertEqual(busca.count(), 1)
        self.assertEqual(busca.first().nome, "Laboratório de Informática")
    def test_busca_parcial(self):
        busca = Chave.partial_search(content="Lab")

        self.assertIsInstance(busca, QuerySet)
        nomes = [c.nome for c in busca]
        self.assertCountEqual(
            nomes,
            ["Laboratório de Informática", "Laboratório de Química"]
        )
class HistoricoBuscaTests(TestCase):
    def setUp(self):
        self.pessoa1 = Pessoa.objects.create(
            matricula=1,
            nome="João",
            cargo= "Professor"
        )

        self.chave1 = Chave.objects.create(nome="Laboratório de Informática")

        self.historico1 = Historico.registrar(
        id_historico=20251105154332,
        acao="RETIRADA",
        id_pessoa=self.pessoa1,
        id_chave=self.chave1,
        horario=datetime.now()
    )
        self.historico2 = Historico.registrar(
        id_historico=20250905154355,
        acao="ATUALIZACAO",
        id_pessoa=self.pessoa1,
        id_chave=self.chave1,
        horario=datetime.now()
    )
    
    def test_busca_por_id(self):
        busca = Historico.search_by_id(id_chave=20251105154332)
        self.assertEqual(self.historico1.id_chave, busca.id_chave)
        self.assertEqual(self.historico1.acao, busca.acao)
        self.assertEqual(self.historico1.id_pessoa, busca.id_pessoa)
    
    def test_devolver_todos_os_registros(self):
        busca = Historico.getAll()
        todos = Historico.objects.all()

        self.assertCountEqual(busca, todos)

class ChaveStatusBuscaTests(TestCase):
    def setUp(self):
        # Cria pessoas
        self.pessoa1 = Pessoa.objects.create(matricula=1, nome="João", cargo="Professor")
        self.pessoa2 = Pessoa.objects.create(matricula=2, nome="Maria", cargo="Técnico")

        # Cria chaves
        self.chave1 = Chave.objects.create(nome="Laboratório 101")
        self.chave2 = Chave.objects.create(nome="Sala de Reunião")
        self.chave3 = Chave.objects.create(nome="Biblioteca")

        # Cria status (chave1 e chave2 estão com pessoas; chave3 está livre)
        self.status1 = ChaveStatus.objects.create(
            id_chave=self.chave1,
            id_pessoa=self.pessoa1,
            checkin=datetime.now()
        )
        self.status2 = ChaveStatus.objects.create(
            id_chave=self.chave2,
            id_pessoa=self.pessoa2,
            checkin=datetime.now()
        )
        self.status3 = ChaveStatus.objects.create(
            id_chave=self.chave3,
            id_pessoa=None,
            checkin=None
        )
    def test_busca_por_chave(self):
        """Busca um status específico pelo id da chave."""
        busca = ChaveStatus.objects.get(id_chave=self.chave1.id)
        self.assertEqual(busca.id_pessoa.nome, "João")
        self.assertFalse(busca.status_code)

    def test_busca_chaves_disponiveis(self):

        busca = ChaveStatus.filter_by_status(status_code=True)
        nomes_chaves = [status.id_chave.nome for status in busca]

        self.assertCountEqual(nomes_chaves, ["Biblioteca"])

    def test_busca_chaves_indisponiveis(self):
        busca = ChaveStatus.filter_by_status(status_code=False)
        nomes_chaves = [status.id_chave.nome for status in busca]
        self.assertCountEqual(nomes_chaves, ["Laboratório 101", "Sala de Reunião"])
