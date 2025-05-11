from django.apps import AppConfig

class ShapesAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shapes_app'

    def ready(self):
        import shapes_app.signals
