"""Modelos (tabelas) da aplicação. (accounts)."""

from django.contrib.auth.models import AbstractUser
from django.db import models

# Classe do projeto.
class CustomUser(AbstractUser):
    PERFIL_CHOICES = (
        ('ADMIN', 'Administrador'),
        ('GERENTE', 'Gerente'),
        ('OPERADOR', 'Operador'),
    )
    
    # Campo único solicitado no requisito (substitui o uso de first_name + last_name na interface)
    nome_completo = models.CharField('Nome completo', max_length=255, default='')

    perfil = models.CharField(max_length=10, choices=PERFIL_CHOICES, default='OPERADOR')
    data_cadastro = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ["email", "nome_completo"]

    # Garante compatibilidade com templates/código que usam get_full_name
    def get_full_name(self):
        return (self.nome_completo or '').strip()

    def __str__(self):
        return f"{self.username} ({self.get_perfil_display()})"
