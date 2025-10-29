from django.test import TestCase
from guarita.models import Pessoa
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