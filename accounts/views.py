"""Views baseadas em classes (CBVs) da aplicação. (accounts)."""

import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from core.mixins import AdminRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, InactivateObjectMixin, PaginateBy20Mixin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser
from .services import inativar_usuario


audit_logger = logging.getLogger('audit')


# View (CBV) responsável pela tela de login de usuários.
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = form.get_user()
        audit_logger.info('LOGIN_OK user=%s', getattr(user, 'username', None))
        return super().form_valid(form)

    def form_invalid(self, form):
        """Trata falhas de login, diferenciando usuário inativo de credenciais inválidas."""
        username = self.request.POST.get('username')
        User = get_user_model()
        usuario = None

        if username:
            try:
                usuario = User.objects.get(username=username)
            except User.DoesNotExist:
                usuario = None

        if usuario is not None and not usuario.is_active:
            # Login falhou porque o usuário existe, mas está inativo
            audit_logger.warning('LOGIN_FAIL_INACTIVE username=%s', username)
            messages.error(
                self.request,
                'Usuário inativo. Entre em contato com o administrador.',
            )
        else:
            # Login falhou por credenciais inválidas (usuário não existe ou senha errada)
            audit_logger.warning('LOGIN_FAIL username=%s', username)
            messages.error(self.request, 'Usuário ou senha inválidos.')

        return super().form_invalid(form)


# View (CBV) responsável por encerrar a sessão do usuário (logout).
class UserLogoutView(LogoutView):
    next_page = 'login'

    def dispatch(self, request, *args, **kwargs):
        audit_logger.info('LOGOUT user=%s', getattr(request.user, 'username', None))
        return super().dispatch(request, *args, **kwargs)


# View (CBV) responsável pela listagem de usuários do sistema.
class UserListView(LoginRequiredMixin, AdminRequiredMixin, PaginateBy20Mixin, ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'usuarios'
    ordering = ("-is_active", "nome_completo")


# View (CBV) responsável por exibir os detalhes de um usuário específico.
class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'usuario'




# View (CBV) responsável pelo cadastro (criação) de novos usuários.
class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, CreateView):
    audit_action = 'CREATE'
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'accounts/user_form.html'
    # As rotas foram registradas diretamente no setup/urls.py (sem include/namespace).
    # Portanto, o sucesso deve redirecionar para o nome da rota global.
    success_url = reverse_lazy('user_list')
    success_message = 'Usuário criado com sucesso!'


# View (CBV) responsável pela edição/atualização de usuários existentes.
class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, AuditLogMixin, FlashSuccessMessageMixin, UpdateView):
    audit_action = 'UPDATE'
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('user_list')
    success_message = 'Usuário atualizado com sucesso!'


# View (CBV) responsável por inativar usuários (soft delete, sem excluir do banco).
class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, InactivateObjectMixin, DeleteView):
    model = CustomUser
    success_url = reverse_lazy('user_list')

    def perform_inactivation(self, obj, user):
        inativar_usuario(obj)

    inactivate_field = 'is_active'
    inactivate_value = False
    success_message = 'Usuário inativado com sucesso!'