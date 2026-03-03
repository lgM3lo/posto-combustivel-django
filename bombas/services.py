"""Camada de serviços: regras de negócio e operações reutilizáveis da aplicação. (bombas)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Set


# Máquina de estados (FSM) para o status da Bomba.
# Centraliza regras de transição para evitar lógica espalhada em views/templates.
ALLOWED_STATUS_TRANSITIONS: Dict[str, Set[str]] = {
    "ATIVA": {"ATIVA", "MANUTENCAO", "INATIVA"},
    "MANUTENCAO": {"MANUTENCAO", "ATIVA", "INATIVA"},
    "INATIVA": {"INATIVA", "ATIVA"},  # regra escolhida: bomba inativa não entra direto em manutenção
}


@dataclass(frozen=True)
# Classe do projeto.
class InvalidStatusTransition(Exception):
    from_status: str
    to_status: str

    def __str__(self) -> str:
        return f"Transição inválida de status: {self.from_status} -> {self.to_status}"


# Função utilitária do projeto.
def validate_status_transition(from_status: str, to_status: str) -> None:
    allowed = ALLOWED_STATUS_TRANSITIONS.get(from_status, set())
    if to_status not in allowed:
        raise InvalidStatusTransition(from_status=from_status, to_status=to_status)
