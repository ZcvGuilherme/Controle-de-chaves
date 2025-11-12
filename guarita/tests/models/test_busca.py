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

    def test_busca_parcial(self):
        busca = Pessoa.partial_search(content="Jo")
        nomes = [p.nome for p in busca]
        self.assertCountEqual(nomes, ["João", "Joana", "Jorge"])

    def test_busca_retorno_todas_as_pessoas(self):
        busca = Pessoa.getAll()
        nomes = [p.nome for p in busca]
        self.assertEqual(busca.count(), 4)
        self.assertCountEqual(nomes, ["João", "Maria", "Joana", "Jorge"])

class ChaveBuscaTests(TestCase):
    def setUp(self):
        self.chave1 = Chave.registrar_chave(nome="Laboratório de Informática")
        self.chave2 = Chave.registrar_chave(nome="Laboratório de Química")
        self.chave3 = Chave.registrar_chave(nome="Biblioteca")


    def test_busca_parcial(self):
        busca = Chave.partial_search(content="Lab")

        self.assertIsInstance(busca, QuerySet)
        nomes = [c.nome for c in busca]
        self.assertCountEqual(
            nomes,
            ["Laboratório de Informática", "Laboratório de Química"]
        )

    def test_busca_parcial_2(self):
        busca1 = Chave.partial_search(content="Lab")
        busca2 = Chave.partial_search("1")
        self.assertIsInstance(busca1, QuerySet)
        nomes = [c.nome for c in busca1]
        nomes2 = [d.nome for d in busca2]

        self.assertCountEqual(
            nomes,
            ["Laboratório de Informática", "Laboratório de Química"]
        )
        self.assertEqual(
            nomes2,
            ["Laboratório de Informática"]
        )
    def test_busca_parcial_numero(self):
        busca = Chave.partial_search(content="1")
        self.assertIsInstance(busca, QuerySet)
        self.assertIn(self.chave1, busca)
        self.assertEqual(busca.count(), 1)

class ChaveStatusBuscaTests(TestCase):
    def setUp(self):
        self.chave1 = Chave.registrar_chave(nome="Laboratório de Informática")
        self.chave2 = Chave.registrar_chave(nome="Sala de Reunião")
        self.pessoa = Pessoa.registrar_pessoa(matricula=1, nome="João", cargo="Professor")

    def test_retorna_todos_os_registros(self):
        resultado = ChaveStatus.getStatus()

        self.assertEqual(resultado.count(), 2)
        self.assertQuerySetEqual(
            resultado.values_list("chave__nome", flat=True),
            ["Laboratório de Informática", "Sala de Reunião"],
            ordered=False
        )

    def test_retorna_com_filtro_por_status(self):
        ChaveStatus.update(self.chave1, self.pessoa, "RETIRADA")

        disponiveis = ChaveStatus.getStatus(status_code=True)

        self.assertEqual(disponiveis.count(), 1)
        self.assertEqual(disponiveis.first().chave.nome, "Sala de Reunião")

        indisponiveis = ChaveStatus.getStatus(status_code=False)
        self.assertEqual(indisponiveis.count(), 1)
        self.assertEqual(indisponiveis.first().chave.nome, "Laboratório de Informática")

    def test_filtrar_por_item_busca_chave(self):
        resultados = ChaveStatus.getStatus(itemBusca="Reu")
        self.assertEqual(resultados.count(), 1)
        self.assertEqual(resultados.first().chave.nome, "Sala de Reunião")

    def test_filtrar_por_item_busca_pessoa(self):
        ChaveStatus.update(self.chave2, self.pessoa, "RETIRADA")

        resultados = ChaveStatus.getStatus(itemBusca="Jo")
        self.assertEqual(resultados.count(), 1)
        self.assertEqual(resultados.first().pessoa.nome, "João")

    def test_filtrar_combinando_filtros(self):
        ChaveStatus.update(self.chave1, self.pessoa, "RETIRADA")

        resultados = ChaveStatus.getStatus(status_code=False, itemBusca="Laboratório")
        self.assertEqual(resultados.count(), 1)
        self.assertEqual(resultados.first().chave.nome, "Laboratório de Informática")

    