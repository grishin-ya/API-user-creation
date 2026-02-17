from django.core.management.base import BaseCommand
from users.models import Direction


class Command(BaseCommand):

    def handle(self, *args, **options):
        directions = [
            "Python",
            "QA",
            "Angular",
            "React",
        ]

        created = 0
        for name in directions:
            obj, was_created = Direction.objects.get_or_create(name=name)
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Создано новых направлений: {created}"
            )
        )
