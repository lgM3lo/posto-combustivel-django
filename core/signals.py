"""Módulo da aplicação/projeto (core)."""

import logging

from django.contrib.auth.signals import user_logged_in, user_login_failed, user_logged_out
from django.dispatch import receiver


audit_logger = logging.getLogger('audit')


@receiver(user_logged_in)
# Função utilitária do projeto.
def log_user_login(sender, request, user, **kwargs):
    audit_logger.info('LOGIN_OK user=%s ip=%s', getattr(user, 'username', None), request.META.get('REMOTE_ADDR'))


@receiver(user_login_failed)
# Função utilitária do projeto.
def log_user_login_failed(sender, credentials, request, **kwargs):
    username = None
    try:
        username = credentials.get('username')
    except Exception:
        pass
    ip = request.META.get('REMOTE_ADDR') if request else None
    audit_logger.warning('LOGIN_FAIL user=%s ip=%s', username, ip)


@receiver(user_logged_out)
# Função utilitária do projeto.
def log_user_logout(sender, request, user, **kwargs):
    audit_logger.info('LOGOUT user=%s ip=%s', getattr(user, 'username', None), request.META.get('REMOTE_ADDR'))
