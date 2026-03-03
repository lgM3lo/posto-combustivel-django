"""Configuração da aplicação para o Django. (core)."""

from django.apps import AppConfig


# Classe do projeto.
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # noqa: F401 - importa sinais para registrar handlers
        from . import signals  # noqa
