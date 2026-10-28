"""Production overrides for the PythonAnywhere WSGI application."""

import os

from django.core.exceptions import ImproperlyConfigured

from .settings import *  # noqa: F403


DEBUG = False

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
if len(SECRET_KEY) < 50:
    raise ImproperlyConfigured('Set DJANGO_SECRET_KEY to a random value of at least 50 characters.')

ALLOWED_HOSTS = [
    host.strip() for host in os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')
    if host.strip()
]
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    raise ImproperlyConfigured('Set DJANGO_ALLOWED_HOSTS to the explicit public hostname(s).')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'  # noqa: F405
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
