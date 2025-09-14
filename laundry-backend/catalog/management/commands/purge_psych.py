from django.core.management.base import BaseCommand
from catalog.models import Service


class Command(BaseCommand):
    help = "Remove any services related to Psychologist/Consultation from the database"

    def handle(self, *args, **options):
        qs = Service.objects.filter(name__icontains="psycholog")
        count = qs.count()
        qs.delete()
        self.stdout.write(self.style.SUCCESS(f"Removed {count} psychologist-related services."))


