from django.apps import AppConfig


class ReminderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reminder'

    def ready(self):
        # We only start the scheduler if we are NOT in the auto-reloader
        # (prevents starting two schedulers in dev mode)
        import os
        if os.environ.get('RUN_MAIN') == 'true':
            from .scheduler import start_reminder_scheduler
            start_reminder_scheduler()
