from django.db import migrations


def create_directions(apps, schema_editor):
    Direction = apps.get_model("users", "Direction")

    directions = [
        "Python",
        "QA",
        "Angular",
        "React",
    ]

    for name in directions:
        Direction.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_directions),
    ]
