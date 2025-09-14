from django.core.management.base import BaseCommand
from catalog.models import Service


class Command(BaseCommand):
    help = "Seed demo services for frontend"

    def handle(self, *args, **options):
        demos = [
            {
                "name": "Wash & Fold",
                "description": "Everyday laundry washed, dried and neatly folded.",
                "price": 99.0,
                "category": "Laundry",
                "is_active": True,
            },
            {
                "name": "Dry Cleaning",
                "description": "Premium dry clean for delicate garments.",
                "price": 199.0,
                "category": "Laundry",
                "is_active": True,
            },
            {
                "name": "Shoe Cleaning",
                "description": "Deep-clean for sneakers and leather shoes.",
                "price": 149.0,
                "category": "Accessories",
                "is_active": True,
            },
            {
                "name": "Premium Wash & Iron",
                "description": "Crisp iron finish with gentle premium wash.",
                "price": 159.0,
                "category": "Laundry",
                "is_active": True,
            },
            {
                "name": "Express 4-Hour",
                "description": "Lightning-fast turnaround for urgent needs.",
                "price": 249.0,
                "category": "Laundry",
                "is_active": True,
            },
            {
                "name": "Delicate Care",
                "description": "Silk, wool, and delicate fabrics handled with care.",
                "price": 219.0,
                "category": "Laundry",
                "is_active": True,
            },
            {
                "name": "Curtain & Blanket Clean",
                "description": "Deep clean for curtains, blankets and home linens.",
                "price": 299.0,
                "category": "Home Care",
                "is_active": True,
            },
        ]

        created = 0
        for data in demos:
            obj, was_created = Service.objects.get_or_create(name=data["name"], defaults=data)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded {created} new services (idempotent)."))


