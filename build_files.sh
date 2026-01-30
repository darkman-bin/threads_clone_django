#!/usr/bin/env bash
set -o errexit

python -m pip install --upgrade pip
pip install -r requirements.txt

# تجميع ملفات static (مهم لـ WhiteNoise و Django admin)
python manage.py collectstatic --noinput

# ملاحظة:
# - على Vercel يفضل استخدام Postgres (DATABASE_URL)
# - تشغيل migrate هنا يعتمد على قاعدة البيانات.
# إذا كنت تستخدم DATABASE_URL (Postgres) وتبي الميجريشن تتم بالبيلد:
# python manage.py migrate --noinput
