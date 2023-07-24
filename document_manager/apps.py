from django.apps import AppConfig


class DocumentManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'document_manager'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Document'))