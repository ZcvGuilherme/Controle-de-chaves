from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Chave, ChaveStatus, Historico, Pessoa
from django.contrib.auth.models import User
@receiver(post_save, sender=Chave)
def criar_status_automatico(sender, instance, created, **kwargs):
    if created:
        ChaveStatus.objects.get_or_create(chave=instance)


@receiver(post_save, sender=Chave)
def gerar_itemBusca(sender, instance, created, **kwargs):
    if created:
        instance.itemBusca = f"Chave {instance.id} - {instance.nome}"
        instance.save(update_fields=["itemBusca"])


@receiver(post_save, sender=User)
def gerar_pessoa_automatico(sender, instance, created, **kwargs):
    if created:
        Pessoa.registrar_pessoa(
            instance.id,
            instance.get_full_name(),
            "",
            instance
        )
        