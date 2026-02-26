"""Configuração da aplicação para o Django. (accounts)."""

from django.apps import AppConfig


# Classe do projeto.
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Contas de Usuário'