from django.db import migrations


def create_categories(apps, schema_editor):
    Categorie = apps.get_model('library', 'Categorie')
    names = [
        'Roman',
        'Fantastique',
        'Classique',
        'Science',
        'Policier',
        'Philosophie',
        'Histoire',
    ]
    for name in names:
        Categorie.objects.get_or_create(nom=name)


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_emprunt'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
