# from django.test import TestCase
# from guarita.models import Pessoa, Chave, Historico, ChaveStatus
# from django.db import IntegrityError
# from django.utils import timezone
# class PessoaInsertModelTest(TestCase):
#     def test_registrar_pessoa(self):
#         Pessoa.registrar_pessoa(matricula= 1, nome= "João", cargo= "Professor")
#         pessoa = Pessoa.objects.first()
#         self.assertEqual(Pessoa.objects.count(), 1)
#         self.assertEqual(pessoa.nome, "João")
#         self.assertEqual(pessoa.cargo, "Professor")
    

#     def test_duplicata_de_pessoa(self):
#         Pessoa.registrar_pessoa(matricula= 1, nome= "João", cargo= "Professor")

#         with self.assertRaises(IntegrityError):
#             Pessoa.registrar_pessoa(1, "Carlos", "Técnico")


# class ChaveInsertModelTest(TestCase):
#     def test_registrar_pessoa(self):
#         Chave.registrar_chave(nome= "Laboratório de Informática")
#         chave = Chave.objects.first()
#         self.assertEqual(Chave.objects.count(), 1)
#         self.assertEqual(chave.nome, "Laboratório de Informática")

# class HistoricoInsertModelTest(TestCase):
#     def setUp(self):
#         self.pessoa = Pessoa.objects.create(
#             matricula = 1,
#             nome="João",
#             cargo="Professor"
#         )
#         self.chave = Chave.objects.create(
#             id=1,
#             nome="Laboratório de Informática"
#         )

#     def test_registrar_acesso_historico(self):
#         Historico.registrar_acesso(
#             acao="RETIRADA",
#             pessoa = self.pessoa,
#             chave= self.chave,
#         )

#         self.assertEqual(Historico.objects.count(), 1)
#         registro = Historico.objects.first()
        
  
#         self.assertEqual(registro.acao, "RETIRADA")
#         self.assertEqual(registro.pessoa.nome, "João")
#         self.assertEqual(registro.chave.nome, "Laboratório de Informática")

    
#     def test_historico_com_pessoa_inexistente(self):
#         with self.assertRaises(ValueError):
#             Historico.registrar_acesso(
#                 acao="RETIRADA",
#                 pessoa=999,
#                 chave=self.chave,
#             )

#     def test_historico_com_chave_inexistente(self):
#         with self.assertRaises(ValueError):
#             Historico.registrar_acesso(
#                 acao="RETIRADA",
#                 pessoa=self.pessoa,
#                 chave=777,
#             )
    
# class ChaveStatusInsertModelTest(TestCase):
#     def setUp(self):
#         self.pessoa = Pessoa.objects.create(
#             matricula=1,
#             nome="João",
#             cargo="Professor"
#         )
#         self.chave = Chave.objects.create(
#             id=1,
#             nome="Laboratório de Informática"
#         )
#         self.chave2 = Chave.registrar_chave("Lab 2")
#     def test_verificar_insert_funciona(self):
#         key = ChaveStatus.criar_status(
#             chave=self.chave
#         )
#         self.assertEqual(self.chave.id, key.chave.id)
#     def test_insert_chave_disponivel(self):
#         status = ChaveStatus.criar_status(
#             chave=self.chave
#         )
#         self.assertTrue(status.status_code)
#         print(f"Status criado: {status.status_code} (esperado: Disponível=True)")

#     def test_verificar_se_registroChave_registra_ChaveStatus(self):

#         self.assertIsInstance(self.chave2, Chave)
#         status = ChaveStatus.objects.filter(chave=self.chave2).first()
#         self.assertIsNotNone(status, "O status da chave não foi criado automaticamente.")
#         self.assertEqual(status.chave, self.chave2)
