"""Camada de serviços: regras de negócio e operações reutilizáveis da aplicação. (funcionarios)."""

from __future__ import annotations

from funcionarios.models import Funcionario


# Função utilitária do projeto.
def inativar_funcionario(funcionario: Funcionario) -> None:
    """Inativação lógica (não exclui do banco)."""
    if funcionario.is_active:
        funcionario.is_active = False
        funcionario.save(update_fields=["is_active"])
