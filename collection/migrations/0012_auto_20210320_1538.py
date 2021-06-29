# Generated by Django 3.1.7 on 2021-03-20 15:38

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0011_auto_20210320_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncard',
            name='set_has_foil',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AddField(
            model_name='collectioncard',
            name='set_languages',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=25), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collectioncard',
            name='set_release_date',
            field=models.DateField(default='2020-01-01'),
            preserve_default=False,
        ),
    ]
