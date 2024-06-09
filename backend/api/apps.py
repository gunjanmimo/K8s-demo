# --------------------------------DJANGO IMPORTS--------------------------------#
from django.apps import AppConfig
from django.core.management import call_command


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"
    scheduler_started = False

    def ready(self):
        """
        This method is called when the Django application is ready to start.
        """

        # Run database migrations every time the server starts
        call_command("migrate")

        # Start the scheduler if it hasn't been started already
        if not ApiConfig.scheduler_started:
            from config import scheduler

            # Start the scheduler
            scheduler.start()

            # Mark the scheduler as started to avoid starting it again
            ApiConfig.scheduler_started = True
