from django.core.management.base import BaseCommand
from ._private import create_patients


class Command(BaseCommand):
    help = 'Populates Users with patients'

    def handle(self, *args, **options):
        create_patients()
        self.stdout.write(self.style.SUCCESS("Succesfully populated User with patients"))



#python manage.py populate_users
