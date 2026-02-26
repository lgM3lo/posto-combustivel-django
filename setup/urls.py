"""Roteamento principal (URL dispatcher) do projeto."""

from django.contrib import admin
from django.urls import include, path

from accounts.views import UserLoginView, UserLogoutView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth (mantido aqui para preservar os nomes "login" e "logout" usados nos templates)
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),

    # Core
    path('', include('core.urls')),

    # Módulos
    path('usuarios/', include('accounts.urls')),
    path('empresa/', include('empresa.urls')),
    path('produtos/', include('produtos.urls')),
    path('bombas/', include('bombas.urls')),
    path('funcionarios/', include('funcionarios.urls')),
]
