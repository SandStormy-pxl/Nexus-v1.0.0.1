import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

if not SECRET_KEY:
    if DEBUG:
        # Chave só para desenvolvimento local. Nunca use em produção.
        SECRET_KEY = 'django-insecure-dev-only-troque-isso'
    else:
        raise RuntimeError(
            'A variável de ambiente SECRET_KEY não foi definida. '
            'Configure-a no seu provedor (ex: Vercel) antes de rodar em produção.'
        )

ALLOWED_HOSTS = [
    h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',') if h.strip()
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'feed',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# -------------------------------------------------------
# BANCO DE DADOS — Supabase via Connection Pooler (6543)
# -------------------------------------------------------
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    if DEBUG:
        # Fallback só para dev local sem Postgres configurado.
        DATABASE_URL = 'sqlite:///' + str(BASE_DIR / 'db.sqlite3')
    else:
        raise RuntimeError(
            'A variável de ambiente DATABASE_URL não foi definida. '
            'Configure-a no seu provedor (ex: Vercel) antes de rodar em produção.'
        )

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=not DATABASE_URL.startswith('sqlite'),
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# -------------------------------------------------------
# ARQUIVOS ESTÁTICOS — WhiteNoise serve no Vercel
# -------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------
# LIMITE DE UPLOAD — 5MB pra não estourar o Supabase free
# -------------------------------------------------------
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB em bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB em bytes
