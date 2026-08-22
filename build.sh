#!/bin/bash

echo "Instalando dependências..."
python -m pip install -r requirements.txt

echo "Executando migrações..."
python manage.py migrate --noinput || true

echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear || true

