from django.apps import AppConfig
# from django.db import connection
from django.core.management import call_command


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    scheduler_started = False 

    def ready(self):
        # run migration every time the server starts
        call_command("migrate")

        if not ApiConfig.scheduler_started :
            from config import scheduler
            scheduler.start()
            ApiConfig.scheduler_started = True  
            
                