"""Mixins reutilizáveis do projeto (permissões, mensagens e auditoria). (core)."""

import logging

from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect




audit_logger = logging.getLogger('audit')


# Mixin reutilizável para compartilhar comportamento entre classes.
class AuditLogMixin:
    """Registra logs de ações críticas (criação/edição/inativação)."""

    audit_action = None  # ex: "CREATE", "UPDATE"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = getattr(self.request, 'user', None)
        audit_logger.info(
            '%s model=%s id=%s user=%s',
            self.audit_action or 'FORM_OK',
            self.model.__name__ if hasattr(self, 'model') and self.model else self.object.__class__.__name__,
            getattr(self.object, 'pk', None),
            getattr(user, 'username', None),
        )
        return response


# Mixin reutilizável para compartilhar comportamento entre classes.
class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.perfil == 'ADMIN'

    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado. Apenas administradores podem acessar esta página.")
        return redirect('dashboard')


# Mixin reutilizável para compartilhar comportamento entre classes.
class GerenteRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.perfil in ['ADMIN', 'GERENTE']

    def handle_no_permission(self):
        messages.error(self.request, "Acesso negado. Você não tem permissão para realizar esta operação.")
        return redirect('dashboard')



# Mixin reutilizável para compartilhar comportamento entre classes.
class PaginateBy20Mixin:
    """Padroniza paginação conforme RNF015."""
    paginate_by = 20


# Mixin reutilizável para compartilhar comportamento entre classes.
class FlashSuccessMessageMixin:
    """Exibe uma mensagem de sucesso após Create/Update."""

    success_message = "Operação realizada com sucesso!"

    def form_valid(self, form):
        response = super().form_valid(form)

        # Evita exibir sucesso em casos onde algum mixin devolveu form_invalid()
        if isinstance(response, HttpResponseRedirect) and self.success_message:
            messages.success(self.request, self.success_message)

        return response


# Mixin reutilizável para compartilhar comportamento entre classes.
class InactivateObjectMixin:
    """Implementa inativação lógica em vez de exclusão.

    Configure:
      - inactivate_field (default: 'is_active')
      - inactivate_value (default: False)
      - audit_action (default: 'INACTIVATE')
      - success_message
      - success_url (ou get_success_url)
    """

    inactivate_field = "is_active"
    inactivate_value = False
    audit_action = "INACTIVATE"
    success_message = "Registro inativado com sucesso!"

    def perform_inactivation(self, obj, user):
        """Implementação padrão de inativação (setar um campo e salvar).

        Views podem sobrescrever para usar uma camada de service.
        """
        setattr(obj, self.inactivate_field, self.inactivate_value)
        obj.save(update_fields=[self.inactivate_field])


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = getattr(request, "user", None)

        # Ponto de extensão: caso a View queira delegar a inativação para um "service"
        # (padrão de organização parecido com o scraper), basta sobrescrever este método.
        self.perform_inactivation(self.object, user)

        user = getattr(request, "user", None)
        audit_logger.info(
            "%s model=%s id=%s user=%s",
            self.audit_action,
            self.object.__class__.__name__,
            getattr(self.object, "pk", None),
            getattr(user, "username", None),
        )

        messages.success(request, self.success_message)

        # compatível com DeleteView (success_url) e genéricos (get_success_url)
        if hasattr(self, "get_success_url"):
            return redirect(self.get_success_url())
        return redirect(self.success_url)