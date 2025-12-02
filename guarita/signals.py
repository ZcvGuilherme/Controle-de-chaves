from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Chave, ChaveStatus, Historico

@receiver(post_save, sender=Chave)
def criar_status_automatico(sender, instance, created, **kwargs):
    if created:
        ChaveStatus.objects.get_or_create(chave=instance)


@receiver(post_save, sender=Chave)
def gerar_itemBusca(sender, instance, created, **kwargs):
    if created:
        instance.itemBusca = f"Chave {instance.id} - {instance.nome}"
        instance.save(update_fields=["itemBusca"])

@receiver(pre_save, sender=ChaveStatus)
def registrar_historico_auto(sender, instance, **kwargs):
    """
    Receiver que registra o histórico automaticamente.
    
    Verifica primeiramente se é uma criação de um status novo

    Tenta  
    """
    if not instance.pk:
        # É criação, não registrar histórico
        return
    
    try:
        #Anterior é a versão do banco de dados, ou seja, a versão que ainda não foi atualizada
        anterior = ChaveStatus.objects.get(pk=instance.pk)
    except ChaveStatus.DoesNotExist:
        return

    # Se pessoa mudou → RETIRADA ou DEVOLUCAO
    if anterior.pessoa != instance.pessoa:

        if instance.pessoa is None:
            acao = "DEVOLUCAO"
            pessoa = anterior.pessoa
        else:
            acao = "RETIRADA"
            pessoa = instance.pessoa

        Historico.registrar_acesso(
            acao=acao,
            pessoa=pessoa,
            chave=instance.chave,
        )