"""Camada de serviços: regras de negócio e operações reutilizáveis da aplicação. (accounts)."""

from __future__ import annotations

from accounts.models import CustomUser


# Função utilitária do projeto.
def inativar_usuario(usuario: CustomUser) -> None:
    """Inativação lógica (não exclui do banco)."""
    if usuario.is_active:
        usuario.is_active = False
        usuario.save(update_fields=["is_active"])
