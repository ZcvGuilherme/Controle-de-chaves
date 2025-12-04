from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
class Pessoa(models.Model):
    """
    <h2>Representação da pessoa no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>Matricula (IntegerField):</b> Chave primária da tabela.\n
    <b>Nome (CharField):</b>  Tamanho máximo de 100 dígitos, representa o nome completo da pessoa. \n
    <b>Cargo (CharField):</b> Tamanho máximo de 100 dígitos. Representa o cargo da pessoa. Sujeito a mudanças. \n
    <b>itemBusca (CharField): </b> Item auto-completável então sem necessidade de colocar seu valor.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    matricula = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    itemBusca = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def registrar_pessoa(cls, matricula, nome, cargo, user):
        return cls.objects.create(matricula=matricula, nome=nome, cargo=cargo, user=user)

    @classmethod
    def partial_search(cls, content):
        """
        <h2>Busca Parcial</h2>\n
        Realiza uma busca não-sensitiva utilizando o nome
        """
        return cls.objects.filter(models.Q(nome__icontains=content))
    
    @classmethod
    def getAll(cls):
        return cls.objects.all()
    
    def save(self, *args, **kwargs):
        self.itemBusca = f"{self.nome} - {self.cargo}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.cargo})"
    
class Chave(models.Model):
    """
    <h2>Representação das chaves no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>id (AutoField):</b> Chave primária da tabela \n
    <b>Nome (CharField):</b>  Tamanho máximo de 100 dígitos, representa o nome da chave. \n
    Ex:. - Laboratório de Informática\n
    <b>itemBusca: </b> Item que deve ser utilizado como string em buscas e exibição em interfaces
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    itemBusca = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def registrar_chave(cls, nome):
        return cls.objects.create(nome=nome)

    @classmethod
    def partial_search(cls, content):
        """
        <h2>Busca Parcial</h2>\n
        Realiza uma busca não-sensitiva utilizando itemBusca como parâmetro.
        """
        return cls.objects.filter(models.Q(itemBusca__icontains=content))
    
    @classmethod
    def getAll(cls):
        return cls.objects.all()
    
    def __str__(self):
        return self.nome


class Historico(models.Model):
    """
    <h2>Representação do histórico no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>id_historico(IntegerField):</b> Chave primária \n

    <b>acao (CharField):</b>  Tamanho máximo de 20 dígitos. Representa a ação feita pela pessoa, sendo eles descritos no atributo ACAO_CHOICES. A idéia é fazer uma espécie de Enum, caso seja necessário, pode-se atualizar o tipo para um mais adequado. \n

    <b>pessoa (ForeignKey):</b> Chave estrangeira importada do objeto Pessoa, on_delete configurado para PROTECT.\n

    <b>chave (ForeignKey):</b> Chave estrangeira importada do objeto Chave, on_delete configurado para PROTECT.\n

    <b>horario (DateTimeField):</b> Vizualização do horário do registro.

    """
    id_historico = models.BigAutoField(primary_key=True)
    
    ACAO_CHOICES = [
        ('RETIRADA', 'Retirada'),
        ('DEVOLUCAO', 'Devolução'),
        ('ATUALIZACAO', 'Atualizacao'),
    ]

    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa'
    )
    chave = models.ForeignKey(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave'
    )
    horario = models.DateTimeField()

    @classmethod
    def registrar_acesso(cls, acao, pessoa, chave):
        agora = timezone.now()
        return cls.objects.create(acao=acao, pessoa=pessoa, chave=chave, horario=agora)

    def __str__(self):
        return f"{self.acao} - {self.pessoa.nome} - {self.chave.nome}"
    

class ChaveStatus(models.Model):
    """
    <h2>Representação do status da chave no banco de dados.</h2>\n
    <p>Esta classe deve ser o alvo das atualizações do status do sistema, o status deve ser atualizado a cada interação e por isso foi colocada fora da abstração da chave, que é uma coisa estática\n

    <h3>Atributos da tabela:</h3> \n
    <b>chave(OneToOneField):</b> Esta é a chave estrangeira importada da tabela Chaves, e pelo fato desta tabela ser uma abstração da chave, este ID também é a chave primária desta tabela.

    <b>pessoa (ForeignKey):</b> Chave estrangeira importada do objeto Pessoa, on_delete configurado para PROTECT.\n

    <b>checkin (DateTimeField):</b> Atributo que deve ser preenchido com o horário que a pessoa capturou a chave. Caso não haja pessoa, ou seja, a chave esteja disponível, valor padrão é vazio\n

    <b>status_code:</b> Representação da disponibilidade da chave. Sendo uma variável Booleana, caso haja uma pessoa com a chave (id_pessoa e checkin preenchidos) o valor deve ser FALSE, logo, "Indisponível". Caso contrário, deve ser TRUE e portanto, "Disponível".

    """
    
    chave = models.OneToOneField(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave',
        primary_key=True
    )

    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa',
        null=True,
        blank=True
    )
    
    checkin = models.DateTimeField(null=True, blank=True)
    status_code = models.BooleanField(editable=False)
    
    @classmethod
    def criar_status(cls, chave):
        status, created = cls.objects.get_or_create(chave=chave)
        return status


    #ChaveStatus.objects.
    # select_related('chave', 'pessoa')
    # .all()
    # .order_by('chave__id')

    @classmethod
    def getStatus(cls, status_code=None, itemBusca=None, order_by="chave__id"):
        """
        <h2> Buscar Status </h2>\n
        Equivalente ao partial_search dos outros, porém esse contém um filtro mais avançado, caso seja colocado sem nenhum parâmetro ele retorna todos os registrosm senão, ele faz uma busca não-sensitiva pelo status code e logo em seguida pelo nome da chave e nome da pessoa.
        """
        query = cls.objects.select_related("chave", "pessoa")

        if status_code is not None:
            query = query.filter(status_code=status_code)

        if itemBusca is not None:
            query = query.filter(
                models.Q(chave__itemBusca__icontains=itemBusca) |
                models.Q(pessoa__itemBusca__icontains=itemBusca)
            )
        if order_by:
            query = query.order_by(order_by)
            
        return query

    
    @classmethod
    def update(cls, chave, pessoa, acao):
        """
        Atualiza o status atual de uma chave e registra a operação no histórico.

        Este método recebe uma `chave`, uma `pessoa` e uma `acao`, valida os dados e 
        aplica a atualização correspondente no status da chave. Também gera um registro 
        no histórico após a operação.

        Parâmetros
        ----------
        chave : Chave
            Instância da chave cujo status será atualizado.
        pessoa : Pessoa
            Pessoa associada à ação realizada (retirada ou devolução).
        acao : str
            A ação a ser executada. Deve ser `"RETIRADA"` ou `"DEVOLUCAO"`.

        Raises
        ------
        ValueError
            - Caso a ação informada seja inválida.
            - Caso a chave já esteja ocupada e seja solicitada uma retirada.
            - Caso a chave esteja disponível e seja solicitada uma devolução.
        TypeError
            - Caso os parâmetros `chave` ou `pessoa` não sejam instâncias válidas 
            de seus respectivos modelos.

        Efeitos Colaterais
        ------------------
        - Atualiza o status da chave no banco de dados.
        - Registra a ação no histórico de acessos.

        """

        #------------------------------VERIFICAR SE AS ENTRADAS SÃO VÁLIDAS---------------------------#
        if acao not in ["RETIRADA", "DEVOLUCAO"]:
            raise ValueError(f"Ação inválida: {acao}. Use 'RETIRADA' ou 'DEVOLUCAO'.")

        if not isinstance(chave, Chave):
            raise TypeError("O parâmetro 'chave' deve ser uma instância válida de Chave.")
        if not isinstance(pessoa, Pessoa):
            raise TypeError("O parâmetro 'pessoa' deve ser uma instância válida de Pessoa.")
        #------------------------------VERIFICAR SE A AÇÃO PODE SER EFETUADA--------------------------#
        status = cls.objects.get(chave=chave)

        if acao == "RETIRADA" and status.pessoa is not None:
            raise ValueError(f"A chave '{status.chave}' já está em uso por {status.pessoa.nome}.")

        if acao == "DEVOLUCAO" and status.pessoa is None:
            raise ValueError(f"A chave '{status.chave}' já está disponível — não há o que devolver.")        
        #------------------------------EFETUAR UPDATE-------------------------------------------------#

        if acao=="DEVOLUCAO":
            status.pessoa = None
            status.checkin = None
            
        else:
            status.pessoa = pessoa
            status.checkin = timezone.now()

        status.save()
        #------------------------------REGISTRAR NO HISTÓRICO-----------------------------------------#
        Historico.registrar_acesso(acao, pessoa, chave)

    def save(self, *args, **kwargs):
        self.status_code = (self.pessoa is None)
        super().save(*args, **kwargs)


    def __str__(self):
        status = "Disponível" if self.status_code else "Em uso"
        if self.pessoa:
            return f"{self.pessoa.nome} - {self.chave.nome} ({status})"
        return f"{self.chave.nome} ({status})"
