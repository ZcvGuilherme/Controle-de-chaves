from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Chave, ChaveStatus, Pessoa
from django.contrib.auth.models import User


@receiver(post_save, sender=Chave)
def criar_status_automatico(sender, instance, created, **kwargs):
    """
    Cria automaticamente o status de uma chave recém-cadastrada.

    Este signal é disparado após o salvamento de uma instância do modelo
    ``Chave``. Quando uma nova chave é criada (``created=True``), é garantido
    que exista um registro correspondente em ``ChaveStatus``.

    Finalidade:
        Inicializar o controle de disponibilidade da chave no sistema,
        evitando que chaves existam sem status associado.

    Args:
        sender (Model): Modelo que disparou o signal (Chave).
        instance (Chave): Instância salva.
        created (bool): Indica se a instância foi criada.
        **kwargs: Argumentos adicionais do signal.
    """
    if created:
        ChaveStatus.objects.get_or_create(chave=instance)


@receiver(post_save, sender=Chave)
def gerar_itemBusca(sender, instance, created, **kwargs):
    """
    Gera automaticamente o campo ``itemBusca`` da chave.

    Executado após o salvamento de ``Chave``. Quando a instância é criada,
    o campo ``itemBusca`` é preenchido com uma string padronizada para
    facilitar buscas textuais no sistema.

    Formato gerado:
        "Chave <id> - <nome>"

    Exemplo:
        "Chave 12 - Laboratório de Informática"

    Args:
        sender (Model): Modelo que disparou o signal (Chave).
        instance (Chave): Instância salva.
        created (bool): Indica se a instância foi criada.
        **kwargs: Argumentos adicionais do signal.
    """
    if created:
        instance.itemBusca = f"Chave {instance.id} - {instance.nome}"
        instance.save(update_fields=["itemBusca"])


@receiver(post_save, sender=Pessoa)
def criar_usuario_para_pessoa(sender, instance, created, **kwargs):
    """
    Cria automaticamente um usuário Django para uma pessoa.

    Disparado após o salvamento de ``Pessoa``. Quando uma nova pessoa é
    cadastrada e não possui usuário associado, um registro é criado em
    ``auth.User``.

    Regras aplicadas:
        - ``username``: matrícula da pessoa.
        - ``password``: matrícula da pessoa (definição provisória).
        - ``first_name``: nome da pessoa.

    Observação:
        A regra de senha deve ser alterada em ambiente de produção por
        motivos de segurança.

    Args:
        sender (Model): Modelo que disparou o signal (Pessoa).
        instance (Pessoa): Instância salva.
        created (bool): Indica se a instância foi criada.
        **kwargs: Argumentos adicionais do signal.
    """
    if created and instance.user is None:
        user = User.objects.create_user(
            username=str(instance.matricula),
            password=str(instance.matricula),  # Mudar regra para senha aqui
            first_name=instance.nome
        )
        instance.user = user
        instance.save()


@receiver(post_save, sender=Pessoa)
def atualizar_usuario(sender, instance, created, **kwargs):
    """
    Sincroniza dados da pessoa com o usuário Django vinculado.

    Sempre que uma instância de ``Pessoa`` é atualizada (``created=False``),
    e existe um usuário associado, o nome da pessoa é refletido no campo
    ``first_name`` do usuário.

    Isso mantém consistência entre os dados pessoais e o cadastro de
    autenticação do sistema.

    Args:
        sender (Model): Modelo que disparou o signal (Pessoa).
        instance (Pessoa): Instância salva.
        created (bool): Indica se a instância foi criada.
        **kwargs: Argumentos adicionais do signal.
    """
    if not created and instance.user:
        instance.user.first_name = instance.nome
        instance.user.save()
