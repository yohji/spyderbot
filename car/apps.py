import sys
from django.apps import AppConfig


class CarConfig(AppConfig):

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'car'

    def ready(self):
        if sys.argv[1:2] != ['test']:

            import car.scheduler as scheduler
            scheduler.start()
