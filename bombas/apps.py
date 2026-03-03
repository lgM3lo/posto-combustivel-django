"""Configuração da aplicação para o Django. (bombas)."""

from django.apps import AppConfig


# Classe do projeto.
class BombasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bombas'
    verbose_name = 'Bombas'
