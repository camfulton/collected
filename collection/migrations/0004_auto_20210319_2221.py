# Generated by Django 3.1.7 on 2021-03-19 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtg', '0021_auto_20210319_2221'),
        ('collection', '0003_auto_20210319_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='cards',
            field=models.ManyToManyField(blank=True, to='mtg.Card'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='sets',
            field=models.ManyToManyField(blank=True, to='mtg.Set'),
        ),
    ]
