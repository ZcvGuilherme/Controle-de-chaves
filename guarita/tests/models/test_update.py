# from django.test import TestCase
# from guarita.models import Pessoa, Chave, Historico, ChaveStatus
# from django.utils import timezone

# #não é prioridade agora
# class PessoaUpdateTests(TestCase):
#    pass

# class ChaveUpdateTests(TestCase):
#     pass
# class HistoricoUpdateTests(TestCase):
#     pass

# class ChaveStatusUpdateTests(TestCase):
#     def setUp(self):
#         self.pessoa1 = Pessoa.objects.create(matricula=1, nome="João", cargo="Professor")
#         self.pessoa2 = Pessoa.objects.create(matricula=2, nome="Maria", cargo="Coordenadora")

#         self.chave = Chave.registrar_chave(nome="Laboratório de Informática")

#             #---------------TESTES DE SUCESSO-------------------#
#     def test_retirar_chave_e_se_gera_historico(self):
        
#         ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="RETIRADA")

#         status = ChaveStatus.objects.get(chave=self.chave)
#         self.assertEqual(status.pessoa, self.pessoa1)
#         self.assertIsNotNone(status.checkin)
#         self.assertFalse(status.status_code)
#         self.assertTrue(Historico.objects.filter(acao="RETIRADA", pessoa=self.pessoa1, chave=self.chave).exists())
    
#     def test_devolucao_chave_e_se_gera_historico(self):
#         ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="RETIRADA")
#         ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="DEVOLUCAO")
        
#         status= ChaveStatus.objects.get(chave=self.chave)
#         status = ChaveStatus.objects.get(chave=self.chave)
#         self.assertIsNone(status.pessoa)
#         self.assertIsNone(status.checkin)
#         self.assertTrue(status.status_code)
#         self.assertTrue(Historico.objects.filter(acao="DEVOLUCAO", pessoa=self.pessoa1, chave=self.chave).exists())


#                 #---------------TESTES DE FALHA-------------------#

#     def test_retirar_chave_em_uso(self):
#         ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="RETIRADA")
#         with self.assertRaises(ValueError) as ctx:
#             ChaveStatus.update(chave=self.chave, pessoa=self.pessoa2, acao="RETIRADA")

#         self.assertIn("já está em uso", str(ctx.exception))


#     def test_devolver_chave_disponivel(self):
#         with self.assertRaises(ValueError) as ctx:
#             ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="DEVOLUCAO")
#         self.assertIn("já está disponível", str(ctx.exception))

#     def test_acao_invalida_lanca_erro(self):
#         with self.assertRaises(ValueError) as ctx:
#             ChaveStatus.update(chave=self.chave, pessoa=self.pessoa1, acao="INVALIDA")
#         self.assertIn("Ação inválida", str(ctx.exception))

#     def test_save_atualiza_status_code_corretamente(self):
#         status = ChaveStatus.objects.get(chave=self.chave)
#         status.pessoa = self.pessoa1
#         status.save()
#         self.assertFalse(status.status_code)

#         status.pessoa = None
#         status.save()
#         self.assertTrue(status.status_code)
