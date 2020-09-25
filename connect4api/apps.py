from django.apps import AppConfig


class Connect4ApiConfig(AppConfig):
    name = 'connect4api'
    
    def ready(self):
        import connect4api.signals