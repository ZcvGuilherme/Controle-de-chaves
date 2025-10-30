from django.db import models

class Pessoa(models.Model):
    """
    <h2>Representação da pessoa no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>Matricula (IntegerField):</b> Chave primária que vamos utilizar. Visto que a matrícula já existe, esse atributo não será autoincrementável.\n
    <b>Nome (CharField):</b>  Tamanho máximo de 100 dígitos, representa o nome completo da pessoa. \n

    <b>Cargo (CharField):</b> Tamanho máximo de 100 dígitos. Representa o cargo da pessoa. Provavelmente futuramente vamos trocar por um Enum, mas por enquanto vamos colocar manualmente os tipos.
    """
    matricula = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    itemBusca = models.CharField(max_length=100)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.itemBusca = f"{self.nome} - {self.cargo}"
        super().save(update_fields=["itemBusca"])

    def __str__(self):

        """
        Equivalente a um to_string() de outras linguagens. Retorna em formato de texto o nome e o cargo do objeto.
        """
        return f"{self.nome} ({self.cargo})"


class Chave(models.Model):
    """
    <h2>Representação das chaves no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>id (AutoField):</b> É uma chave primária autoincrementável\n
    <b>Nome (CharField):</b>  Tamanho máximo de 100 dígitos, representa o nome da chave. \n
    Ex:. - Laboratório de Informática
    <b>itemBusca</b> Item que deve ser utilizado como string em buscas e exibição em interfaces
    """
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    itemBusca = models.CharField(max_length=100)
    """
    Equivalente a um to_string() de outras linguagens. Retorna em formato de texto o nome do objeto.
    """

    """
    <h2>Método Sobrescrevido: save()</h2>
    Este método roda quando o django cria a tabela, portanto, quando for atualizado algum valor este método precis ser rodado novamente
    """
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.itemBusca = f"Chave {self.id} - {self.nome}"
        super().save(update_fields=["itemBusca"])

    def __str__(self):
        return self.nome


class Historico(models.Model):
    """
    <h2>Representação do histórico no banco de dados.</h2>\n
    <h3>Atributos da tabela:</h3> \n
    <b>id_historico(IntegerField):</b> Chave primária que vamos utilizar. Não será autoincrementável. A lógica que deve ser implementada na criação de um registro deve ser o ano, mês, dia, hora, minuto e segundo. Todos representados no mesmo número.\n
    Ex:. 2025-11-05 15:43:32 ---> 20251105154332\n
    <b>acao (CharField):</b>  Tamanho máximo de 20 dígitos. Representa a ação feita pela pessoa, sendo eles descritos no atributo ACAO_CHOICES. A idéia é fazer uma espécie de Enum, caso seja necessário, pode-se atualizar o tipo para um mais adequado. \n

    <b>id_pessoa (ForeignKey):</b> Chave estrangeira importada do objeto Pessoa, on_delete configurado para PROTECT.\n

    <b>id_chave (ForeignKey):</b> Chave estrangeira importada do objeto Chave, on_delete configurado para PROTECT.\n

    <b>horario (DateTimeField):</b> Para uma facilidade de vizualização do horário, coloquei esse atributo que representa o horário, sujeito a ser deletado por redundância.

    """
    id_historico = models.IntegerField(primary_key=True)
    
    ACAO_CHOICES = [
        ('RETIRADA', 'Retirada'),
        ('DEVOLUCAO', 'Devolução'),
        ('ATUALIZACAO', 'Atualizacao'),
    ]

    acao = models.CharField(max_length=20, choices=ACAO_CHOICES)

    id_pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa'
    )
    id_chave = models.ForeignKey(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave'
    )
    horario = models.DateTimeField()

    def __str__(self):
        return f"{self.acao} - {self.id_pessoa.nome} - {self.id_chave.nome}"


class ChaveStatus(models.Model):
    """
    <h2>Representação do status da chave no banco de dados.</h2>\n
    <p>Esta classe deve ser o alvo das atualizações do status do sistema, o status deve ser atualizado a cada interação e por isso foi colocada fora da abstração da chave, que é uma coisa estática\n

    <h3>Atributos da tabela:</h3> \n
    <b>id_chave(OneToOneField):</b> Esta é a chave estrangeira importada da tabela Chaves, e pelo fato desta tabela ser uma abstração da chave, este ID também é a chave primária desta tabela.

    <b>id_pessoa (ForeignKey):</b> Chave estrangeira importada do objeto Pessoa, on_delete configurado para PROTECT.\n

    <b>checkin (DateTimeField):</b> Atributo que deve ser preenchido com o horário que a pessoa capturou a chave. Caso não haja pessoa, ou seja, a chave esteja disponível, colocar valor padrão como NULL (SQL)\n

    <b>status_code:</b> Representação da disponibilidade da chave. Sendo uma variável Booleana, caso haja uma pessoa com a chave (id_pessoa e checkin preenchidos) o valor deve ser FALSE, logo, "Indisponível". Caso contrário, deve ser TRUE e portanto, "Disponível".

    """
    
    id_chave = models.OneToOneField(
        Chave,
        on_delete=models.PROTECT,
        db_column='Id_chave',
        primary_key=True
    )

    id_pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.PROTECT,
        db_column='Id_pessoa',
        null=True,
        blank=True
    )
    
    checkin = models.DateTimeField(null=True, blank=True)
    status_code = models.BooleanField(editable=False)

    class Meta:
        """
        Classe de suporte para evitar duplicação de combinação pessoa + chave
        """
        unique_together = ('id_pessoa', 'id_chave')

    def save(self, *args, **kwargs):
        """
        Método que decide automáticamente se o status_code é true ou false.

        <h1>NOTA IMPORTANTE SOBRE ESSE MÉTODO</h1>

        <p>
        Este método <b> NÃO </b> é chamado em todos os casos. Em métodos como o da criação da instãnica ele vai ser chamado, mas em casos como <b>update</b> ele <b>não é chamado</b> <b>e deve ser chamado manualmente</b> 
        </p>

        """
        self.status_code = (self.id_pessoa is None or self.checkin is None)
        super().save(*args, **kwargs)


    def __str__(self):
        status = "Ativo" if self.status_code else "Inativo"
        return f"{self.id_pessoa.nome} - {self.id_chave.nome} ({status})"
