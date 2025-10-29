from django.test import TestCase
from guarita.models import Pessoa, Chave
from django.db import IntegrityError
class PessoaModelTest(TestCase):
    def teste_registrar_pessoa(self):
        Pessoa.registrar_pessoa(matricula= 1, nome= "João", cargo= "Professor")
        
        self.assertEqual(Pessoa.objects.count(), 1)
        self.assertEqual(Pessoa.nome, "João")
        self.assertEqual(Pessoa.cargo, "Professor")
    

    def teste_duplicata_de_pessoa(self):
        Pessoa.registrar_pessoa(matricula= 1, nome= "João", cargo= "Professor")

        with self.assertRaises(IntegrityError):
            Pessoa.registrar_pessoa(1, "Carlos", "Técnico")


class ChaveModelTest(TestCase):
    def teste_registrar_pessoa(self):
        Chave.registrar_chave(nome= "Laboratório de Informática")

        self.assertEqual(Chave.objects.count(), 1)
        self.assertEqual(Chave.nome, "Laboratório de Informática")

