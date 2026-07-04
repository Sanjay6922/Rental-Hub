from django.core.management.base import BaseCommand
from user_app.views import send_return_reminders

class Command(BaseCommand):
    help = "Send vehicle return reminder emails"

    def handle(self, *args, **kwargs):
        send_return_reminders()
        self.stdout.write(
            self.style.SUCCESS(
                "Reminder emails sent successfully"
            )
        )