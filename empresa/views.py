"""Views baseadas em classes (CBVs) da aplicação. (empresa)."""

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView

from core.mixins import GerenteRequiredMixin, AuditLogMixin
from .models import Empresa


# View (CBV) responsável por exibir os dados cadastrados da empresa.
class EmpresaDetailView(GerenteRequiredMixin, DetailView):
    """Exibe os dados da empresa (singleton)."""

    model = Empresa
    template_name = 'empresa/empresa_detail.html'
    context_object_name = 'empresa'

    def get(self, request, *args, **kwargs):
        # Se não houver empresa cadastrada, direciona para o cadastro
        if not Empresa.objects.exists():
            messages.info(request, "Cadastre os dados da empresa para continuar.")
            return redirect('empresa_create')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Empresa.objects.first()


# View (CBV) responsável por esta funcionalidade.
class EmpresaCreateView(GerenteRequiredMixin, AuditLogMixin, CreateView):
    """Cadastro da empresa (apenas 1 registro)."""

    audit_action = 'CREATE'
    model = Empresa
    fields = '__all__'
    template_name = 'empresa/empresa_form.html'
    success_url = reverse_lazy('empresa_detail')

    def dispatch(self, request, *args, **kwargs):
        # Garante singleton: apenas 1 empresa
        if Empresa.objects.exists():
            return redirect('empresa_update')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Empresa cadastrada com sucesso!")
        return super().form_valid(form)


# View (CBV) responsável por editar/atualizar os dados da empresa.
class EmpresaUpdateView(GerenteRequiredMixin, AuditLogMixin, UpdateView):
    """Edição dos dados da empresa (singleton)."""

    audit_action = 'UPDATE'
    model = Empresa
    fields = '__all__'
    template_name = 'empresa/empresa_form.html'
    success_url = reverse_lazy('empresa_detail')

    def get(self, request, *args, **kwargs):
        if not Empresa.objects.exists():
            return redirect('empresa_create')
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Empresa.objects.first()

    def form_valid(self, form):
        messages.success(self.request, "Empresa atualizada com sucesso!")
        return super().form_valid(form)