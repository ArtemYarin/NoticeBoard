from django.apps import AppConfig


class BoardappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boardapp'

    def ready(self):
        import boardapp.signals


