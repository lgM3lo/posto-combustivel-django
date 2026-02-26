"""Views baseadas em classes (CBVs) da aplicação. (funcionarios)."""

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.mixins import GerenteRequiredMixin, AuditLogMixin, PaginateBy20Mixin, FlashSuccessMessageMixin, InactivateObjectMixin
from .models import Funcionario
from .forms import FuncionarioForm
from .filter import FuncionarioFilter
from .services import inativar_funcionario

audit_logger = logging.getLogger('audit')


# View (CBV) responsável por listar funcionários (com filtros e paginação).
class FuncionarioListView(LoginRequiredMixin, PaginateBy20Mixin, ListView):
    model = Funcionario
    template_name = 'funcionarios/funcionario_list.html'
    context_object_name = 'funcionarios'
    def get_queryset(self):
        base_qs = Funcionario.objects.all().order_by('nome_completo')

        # Comportamento padrão (como antes): exibe apenas ativos caso não seja informado.
        data = self.request.GET.copy()
        if not data.get('is_active'):
            data['is_active'] = 'true'

        self.filterset = FuncionarioFilter(data=data, queryset=base_qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = getattr(self, 'filterset', None)
        return context


# View (CBV) responsável por exibir detalhes de um funcionário específico.
class FuncionarioDetailView(LoginRequiredMixin, DetailView):
    model = Funcionario
    template_name = 'funcionarios/funcionario_detail.html'
    context_object_name = 'funcionario'




# View (CBV) responsável pelo cadastro (criação) de novos funcionários.
class FuncionarioCreateView(LoginRequiredMixin, GerenteRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, CreateView):
    audit_action = 'CREATE'
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionarios/funcionario_form.html'
    # As rotas foram registradas diretamente no setup/urls.py (sem include/namespace).
    success_url = reverse_lazy('funcionario_list')

    def perform_inactivation(self, obj, user):
        inativar_funcionario(obj)

    success_message = 'Funcionário cadastrado com sucesso!'


# View (CBV) responsável pela edição/atualização dos dados de funcionários.
class FuncionarioUpdateView(LoginRequiredMixin, GerenteRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, UpdateView):
    audit_action = 'UPDATE'
    model = Funcionario
    form_class = FuncionarioForm
    template_name = 'funcionarios/funcionario_form.html'
    success_url = reverse_lazy('funcionario_list')

    success_message = 'Funcionário atualizado com sucesso!'


# View (CBV) responsável por inativar funcionários (sem excluir do banco).
class FuncionarioDeleteView(LoginRequiredMixin, GerenteRequiredMixin, InactivateObjectMixin, DeleteView):
    model = Funcionario
    success_url = reverse_lazy('funcionario_list')

    inactivate_field = 'is_active'
    inactivate_value = False
    success_message = 'Funcionário inativado com sucesso!'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save(update_fields=['is_active'])
        audit_logger.info('INACTIVATE model=Funcionario id=%s user=%s', self.object.pk, getattr(request.user, 'username', None))
        messages.success(request, 'Funcionário inativado com sucesso!')
        return redirect(self.success_url)