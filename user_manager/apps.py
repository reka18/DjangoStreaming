from django.apps import AppConfig


class UserManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user_manager'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('StreamUser'))
        from django.contrib.auth.models import User
        registry.register(User)