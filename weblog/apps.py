from django.apps import AppConfig
import os

class WeblogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'weblog'
    path = os.path.join(os.path.dirname(__file__))
