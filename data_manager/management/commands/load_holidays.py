from django.core.management.base import BaseCommand, CommandError
from data_manager.models import Events

class Command(BaseCommand):

    def handle(self, *args, **options):
        

            # self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))