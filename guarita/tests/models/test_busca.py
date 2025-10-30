from django.test import TestCase
from guarita.models import Pessoa, Chave, Historico, ChaveStatus
from django.db.models.query import QuerySet
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
        self.assertQuerySetEqual(busca, [self.pessoa1, self.pessoa3, self.pessoa4], ordered=False)
    #métodos de busca:
    #receber uma QuerySet
    #critérios: 

  
    #buscar por cargo
    #busca parcial
    #buscar todos
   

class ChaveBuscaTests(TestCase):
    #Atributos:
    #id
    #nome

    #métodos de busca:
    #receber uma Query
    pass
class HistoricoBuscaTests(TestCase):
    #Atributos:
    #id_historico
    #nome

    #métodos de busca:
    #receber o objeto Chave inteiro
    pass

class ChaveStatusBuscaTests(TestCase):
    pass