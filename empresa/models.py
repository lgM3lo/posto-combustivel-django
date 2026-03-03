"""Modelos (tabelas) da aplicação. (empresa)."""

from django.db import models
from core.validators import validate_cnpj

# Classe do projeto.
class Empresa(models.Model):
    razao_social = models.CharField(max_length=255)
    nome_fantasia = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validate_cnpj])
    inscricao_estadual = models.CharField(max_length=20)
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
    
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome_fantasia
