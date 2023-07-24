from django.apps import AppConfig


class TagManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tag_manager'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Tag'))