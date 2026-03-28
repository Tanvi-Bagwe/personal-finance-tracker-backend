from django.apps import AppConfig


class ReminderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reminder'

    def ready(self):
        from .scheduler import start_reminder_scheduler
        start_reminder_scheduler()
