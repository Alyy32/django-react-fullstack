from django.apps import AppConfig


class RedisDemoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core.redis_demo'
    verbose_name = 'Redis Demo'
