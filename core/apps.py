from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        # يربط إشارات إنشاء Profile تلقائياً
        from . import signals  # noqa
