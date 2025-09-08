from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# Validator for phone numbers - REMOVED FOR FLEXIBILITY
# phone_regex = RegexValidator(
#     regex=r'^[0-9]{9}$',
#     message="O número de telefone deve ter exatamente 9 dígitos."
# )

class PessoaBase(models.Model):
    nome = models.CharField(max_length=255, unique=True, verbose_name="Nome Completo")
    nuit = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="NUIT")
    tipoDeIdentificacao = models.CharField(max_length=255, choices=[
        ("BI", "BI"),
        ("Passaporte", "Passaporte"),
        ("Carta de conducao", "Carta de condução"),
        ("Outro", "Outro")
    ], null=True, blank=True, verbose_name="Tipo de Identificação")
    numeroDeIdentificacao = models.CharField(max_length=255, verbose_name="Número de Identificação")
    residencia = models.CharField(max_length=255, verbose_name="Residência")
    email = models.EmailField(max_length=255, null=True, blank=True)
    localDeTrabalho = models.CharField(max_length=255, null=True, blank=True, verbose_name="Local de Trabalho")
    telefone = models.CharField(max_length=20, null=True, blank=True, unique=True)
    telefone1 = models.CharField(max_length=20, null=True, blank=True)
    telefone2 = models.CharField(max_length=20, null=True, blank=True)
    estadoCivil = models.CharField(max_length=255, choices=[
        ("Solteiro", "Solteiro"),
        ("Solteira", "Solteira"),
        ("Casado", "Casado"),
        ("Casada", "Casada"),
        ("Separado Judicialmente", "Separado Judicialmente"),
        ("Separada Judicialmente", "Separada Judicialmente"),
        ("Outro", "Outro")
    ], null=True, blank=True, verbose_name="Estado Civil")
    dataDeExpiracao = models.DateField(null=True, blank=True, verbose_name="Data de Expiração")
    dataDeEmissao = models.DateField(null=True, blank=True, verbose_name="Data de Emissão")

    class Meta:
        abstract = True

    def __str__(self):
        return self.nome


class Cliente(PessoaBase):
    codigo = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Código do Cliente")
    nomeDoArquivoDeIdentificacao = models.CharField(max_length=255, null=True, blank=True,
                                                    verbose_name="Nome do Arquivo de Identificação")
    nacionalidade = models.CharField(max_length=255, null=True, blank=True)
    dataDeNascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    profissao = models.CharField(max_length=255, null=True, blank=True, verbose_name="Profissão")
    genero = models.CharField(max_length=255, choices=[
        ("masculino", "masculino"),
        ("feminino", "feminino"),
        ("transgenero", "transgênero"),
        ("nao-binario", "não-binário"),
        ("agenero", "agênero"),
        ("pangenero", "pangênero"),
        ("genderqueer", "genderqueer"),
        ("two-spirit", "two-spirit"),
        ("outro", "outro")
    ], null=True, blank=True, verbose_name="Gênero")
    classificacao = models.CharField(max_length=255, choices=[
        ("excelente", "excelente"),
        ("bom", "bom"),
        ("medio", "medio"),
        ("mau", "mau"),
        ("pessimo", "pessimo")
    ], null=True, blank=True, default="medio", verbose_name="Classificação")
    ativo = models.BooleanField(default=True)
    emDivida = models.BooleanField(default=False, verbose_name="Em Dívida")
    totalEmDivida = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, verbose_name="Total em Dívida")
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilizador")
    last_updated = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # Relação Many-to-Many corrigida
    assinantes = models.ManyToManyField(
        'Assinante',
        related_name='clientes',
        verbose_name="Assinantes"
    )

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Assinante(PessoaBase):
    # O campo de relacionamento foi removido daqui e colocado no Cliente,
    # já que a relação é Many-to-Many.
    utilizador = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Utilizador")

    class Meta:
        verbose_name = "Assinante"
        verbose_name_plural = "Assinantes"