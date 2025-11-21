from django.apps import AppConfig


class GuaritaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'guarita'

    def ready(self):
        import guarita.signals