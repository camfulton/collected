# Generated by Django 3.1.7 on 2021-03-19 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mtg', '0015_auto_20210319_0428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='printing',
            name='uuid',
            field=models.UUIDField(unique=True),
        ),
        migrations.AlterField(
            model_name='set',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
