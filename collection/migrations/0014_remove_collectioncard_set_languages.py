# Generated by Django 3.1.7 on 2021-03-20 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0013_remove_collectioncard_set_has_foil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collectioncard',
            name='set_languages',
        ),
    ]