"""Views baseadas em classes (CBVs) da aplicação. (bombas)."""

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from core.mixins import GerenteRequiredMixin, AuditLogMixin, PaginateBy20Mixin, FlashSuccessMessageMixin, InactivateObjectMixin
from .models import Bomba
from .services import validate_status_transition, InvalidStatusTransition
from .filter import BombaFilter
from produtos.models import Produto


audit_logger = logging.getLogger('audit')


# View (CBV) responsável por esta funcionalidade.
class BombaListView(LoginRequiredMixin, PaginateBy20Mixin, ListView):
    model = Bomba
    template_name = 'bombas/bomba_list.html'
    context_object_name = 'bombas'
    def get_queryset(self):
        base_qs = Bomba.objects.all().select_related('produto').order_by('numero')
        self.filterset = BombaFilter(data=self.request.GET, queryset=base_qs)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = getattr(self, 'filterset', None)
        context['status_choices'] = Bomba.STATUS_CHOICES
        context['produtos'] = Produto.objects.filter(is_active=True).order_by('nome')
        return context


# View (CBV) responsável por exibir detalhes de uma bomba específica.
class BombaDetailView(LoginRequiredMixin, DetailView):
    model = Bomba
    template_name = 'bombas/bomba_detail.html'
    context_object_name = 'bomba'


# View (CBV) responsável pelo cadastro (criação) de novas bombas.
class BombaCreateView(LoginRequiredMixin, GerenteRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, CreateView):
    audit_action = 'CREATE'
    model = Bomba
    fields = '__all__'
    template_name = 'bombas/bomba_form.html'
    success_url = reverse_lazy('bomba_list')

    success_message = 'Bomba cadastrada com sucesso!'


# View (CBV) responsável pela edição/atualização dos dados de uma bomba.
class BombaUpdateView(LoginRequiredMixin, GerenteRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, UpdateView):
    audit_action = 'UPDATE'
    model = Bomba
    fields = '__all__'
    template_name = 'bombas/bomba_form.html'
    success_url = reverse_lazy('bomba_list')

    def form_valid(self, form):
        # FSM: valida transição de status antes de salvar
        old_status = self.get_object().status
        new_status = form.cleaned_data.get('status')
        if old_status != new_status:
            try:
                validate_status_transition(old_status, new_status)
            except InvalidStatusTransition as exc:
                form.add_error('status', str(exc))
                return self.form_invalid(form)
        return super().form_valid(form)

    success_message = 'Bomba atualizada com sucesso!'


# View (CBV) responsável por inativar bombas (alterando o status para INATIVA).
class BombaDeleteView(LoginRequiredMixin, GerenteRequiredMixin, InactivateObjectMixin, DeleteView):
    model = Bomba
    success_url = reverse_lazy('bomba_list')

    inactivate_field = 'status'
    inactivate_value = 'INATIVA'
    success_message = 'Bomba inativada com sucesso!'