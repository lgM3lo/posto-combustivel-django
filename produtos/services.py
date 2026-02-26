"""Camada de serviços: regras de negócio e operações reutilizáveis da aplicação. (produtos)."""

from __future__ import annotations

from produtos.models import Produto


# Função utilitária do projeto.
def inativar_produto(produto: Produto) -> None:
    """Inativação lógica (não exclui do banco)."""
    if produto.is_active:
        produto.is_active = False
        produto.save(update_fields=["is_active"])
