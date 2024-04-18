from django.apps import AppConfig


class RevaaRdsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'frontend'

    def ready(self):
        import frontend.signals