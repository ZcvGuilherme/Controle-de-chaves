from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Chave, ChaveStatus

@receiver(post_save, sender=Chave)
def criar_status_automatico(sender, instance, created, **kwargs):
    if created:
        ChaveStatus.objects.get_or_create(chave=instance)


@receiver(post_save, sender=Chave)
def gerar_itemBusca(sender, instance, created, **kwargs):
    if created:
        instance.itemBusca = f"Chave {instance.id} - {instance.nome}"
        instance.save(update_fields=["itemBusca"])