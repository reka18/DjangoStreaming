from django.apps import AppConfig


class ConversationManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversation_manager'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Comment'))
        registry.register(self.get_model('Message'))
