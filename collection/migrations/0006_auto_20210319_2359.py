# Generated by Django 3.1.7 on 2021-03-19 23:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0005_collection_border'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='border',
            field=models.IntegerField(blank=True, choices=[(1, 'Old Border'), (2, 'Modern Border'), (3, 'Futureshifted'), (4, 'Magic 2015')], null=True),
        ),
    ]
