import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------
# SECRET KEY — Fallback seguro para evitar erro 500 no boot
# -------------------------------------------------------
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-nexus-prod-fallback-change-in-vercel-env-vars-998877'
)

# -------------------------------------------------------
# DEBUG & ALLOWED HOSTS
# -------------------------------------------------------
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')

raw_hosts = os.environ.get('ALLOWED_HOSTS', '*')
if raw_hosts == '*':
    ALLOWED_HOSTS = ['*']
else:
    # Remove https://, http:// e barras caso tenham sido colocadas na env var
    ALLOWED_HOSTS = [
        h.strip().replace('https://', '').replace('http://', '').rstrip('/')
        for h in raw_hosts.split(',')
        if h.strip()
    ]
    for default_host in ['.vercel.app', '.now.sh', 'localhost', '127.0.0.1']:
        if default_host not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(default_host)

# -------------------------------------------------------
# CSRF & PROXY (Necessário no Vercel / HTTPS)
# -------------------------------------------------------
CSRF_TRUSTED_ORIGINS = [
    'https://*.vercel.app',
    'https://*.now.sh',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
raw_csrf = os.environ.get('CSRF_TRUSTED_ORIGINS', '')
if raw_csrf:
    for origin in raw_csrf.split(','):
        origin = origin.strip()
        if origin:
            if not origin.startswith(('http://', 'https://')):
                origin = f'https://{origin}'
            if origin not in CSRF_TRUSTED_ORIGINS:
                CSRF_TRUSTED_ORIGINS.append(origin)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# -------------------------------------------------------
# APLICAÇÕES & MIDDLEWARE
# -------------------------------------------------------
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

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=int(os.environ.get('CONN_MAX_AGE', '0')),
            ssl_require=not (DATABASE_URL.startswith('sqlite') or '127.0.0.1' in DATABASE_URL or 'localhost' in DATABASE_URL),
        )
    }
    # Supabase Transaction Pooler (porta 6543) requer desativar server-side cursors
    if 'postgresql' in DATABASES['default'].get('ENGINE', ''):
        DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True
else:
    # Se DATABASE_URL não foi informada, usa SQLite temporário (/tmp em serverless)
    db_file = '/tmp/db.sqlite3' if os.environ.get('VERCEL') == '1' else str(BASE_DIR / 'db.sqlite3')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': db_file,
        }
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
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_USE_FINDERS = True

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedStaticFilesStorage',
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------
# LIMITE DE UPLOAD
# -------------------------------------------------------
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB em bytes
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB em bytes

# -------------------------------------------------------
# AUTENTICAÇÃO
# -------------------------------------------------------
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'


