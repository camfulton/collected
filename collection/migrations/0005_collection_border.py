# Generated by Django 3.1.7 on 2021-03-19 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0004_auto_20210319_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='border',
            field=models.CharField(blank=True, choices=[(1, 'Old Border'), (2, 'Modern Border'), (3, 'Futureshifted'), (4, 'Magic 2015')], max_length=6),
        ),
    ]
