"""Modelos (tabelas) da aplicação. (funcionarios)."""

from django.db import models
from datetime import date
from core.validators import validate_cpf

# Classe do projeto.
class Funcionario(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    rg = models.CharField(max_length=20)
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=20)
    email = models.EmailField()
    
    # Endereço
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    
    cargo = models.CharField(max_length=100)
    data_admissao = models.DateField()
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    @property
    def tempo_empresa(self):
        today = date.today()
        delta = today - self.data_admissao
        anos = delta.days // 365
        meses = (delta.days % 365) // 30
        return f"{anos} anos e {meses} meses"

    def __str__(self):
        return self.nome_completo
