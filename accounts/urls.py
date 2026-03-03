"""Roteamento (URL dispatcher) da aplicação. (accounts)."""

from django.urls import path
from . import views


urlpatterns = [
    # Rotas recomendadas (padrão do sistema)
    path('', views.UserListView.as_view(), name='user_list'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('novo/', views.UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/editar/', views.UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/deletar/', views.UserDeleteView.as_view(), name='user_delete'),

    # Rotas "legadas" (mantidas por compatibilidade / referência)
    path('_legacy/', views.UserListView.as_view(), name='index'),
    path('_legacy/tabela/', views.UserListView.as_view(), name='table'),
    path('_legacy/incluir/', views.UserCreateView.as_view(), name='create'),
    path('_legacy/atualizar/<int:pk>/', views.UserUpdateView.as_view(), name='update'),
    path('_legacy/excluir/<int:pk>/', views.UserDeleteView.as_view(), name='delete'),
]
