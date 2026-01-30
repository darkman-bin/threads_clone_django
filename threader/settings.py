import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ✅ مهم: غيّر SECRET_KEY في Vercel عبر Environment Variables
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-change-me-please")

# DEBUG عبر ENV: اجعلها 0 في الإنتاج
DEBUG = os.environ.get("DEBUG", "1") == "1"

# ===== Hosts / CSRF =====
# في بيئات مثل CloudShell/Vercel الدومين يتغير — نستخدم ENV + قيم افتراضية للتطوير
ALLOWED_HOSTS = []
env_allowed = os.environ.get("ALLOWED_HOSTS", "").strip()
if env_allowed:
    ALLOWED_HOSTS = [h.strip() for h in env_allowed.split() if h.strip()]

# افتراضي للتطوير
if DEBUG and not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = []
env_csrf = os.environ.get("CSRF_TRUSTED_ORIGINS", "").strip()
if env_csrf:
    CSRF_TRUSTED_ORIGINS = [o.strip() for o in env_csrf.split() if o.strip()]

# Vercel يوفر VERCEL_URL مثل: myapp.vercel.app (بدون https)
VERCEL_URL = os.environ.get("VERCEL_URL", "").strip()
if VERCEL_URL:
    # السماح للدومين
    if VERCEL_URL not in ALLOWED_HOSTS and "*" not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(VERCEL_URL)
    # إضافة Origin موثوق
    origin = f"https://{VERCEL_URL}"
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)

# Google CloudShell / web preview domains
# مثال: https://8000-xxxx.cloudshell.dev
# نضيف wildcard للتطوير لتفادي خطأ (403) Origin checking failed
if DEBUG:
    for o in ["https://*.cloudshell.dev", "https://*.vercel.app"]:
        if o not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(o)

# خلف البروكسي (مثل Vercel) لضمان معرفة https
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "core.apps.CoreConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # WhiteNoise يساعد في تقديم static في الإنتاج (مع collectstatic)
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "threader.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "threader.wsgi.application"

# ===== Database =====
# افتراضي: SQLite محلي
# للإنتاج على Vercel يُفضّل Postgres (Vercel Postgres / Neon / Supabase)
# ضع DATABASE_URL في Environment Variables ليتم استخدامها تلقائياً.
DATABASE_URL = os.environ.get("DATABASE_URL", "").strip()
IS_VERCEL = os.environ.get("VERCEL") == "1" or bool(os.environ.get("VERCEL_ENV"))

if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=not DEBUG,
        )
    }
else:
    # SQLite للتطوير المحلي، وعلى Vercel نستخدم /tmp (نظام ملفات للقراءة/الكتابة مؤقت)
    sqlite_name = "/tmp/db.sqlite3" if IS_VERCEL else (BASE_DIR / "db.sqlite3")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": sqlite_name,
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "ar"
TIME_ZONE = "Asia/Muscat"

USE_I18N = True
USE_TZ = True

# ===== Static / Media =====
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

# WhiteNoise storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "feed"
LOGOUT_REDIRECT_URL = "home"

# رسائل Bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: "secondary",
    messages.INFO: "info",
    messages.SUCCESS: "success",
    messages.WARNING: "warning",
    messages.ERROR: "danger",
}

# كوكيز آمنة عند الإنتاج
if not DEBUG:
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_REFERRER_POLICY = "same-origin"
