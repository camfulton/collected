# Generated by Django 3.1.7 on 2021-03-20 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0010_auto_20210320_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectioncard',
            name='artist',
            field=models.CharField(max_length=50),
        ),
    ]
