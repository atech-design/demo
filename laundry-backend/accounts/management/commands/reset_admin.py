from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create or reset the admin user (username=admin) with given password"

    def add_arguments(self, parser):
        parser.add_argument("password", nargs="?", default="Admin@123")

    def handle(self, *args, **options):
        User = get_user_model()
        user, _created = User.objects.get_or_create(
            username="admin", defaults={"email": "admin@example.com"}
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(options["password"])
        user.save()
        self.stdout.write(self.style.SUCCESS("Admin credentials reset."))


