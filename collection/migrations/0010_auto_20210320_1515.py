# Generated by Django 3.1.7 on 2021-03-20 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0009_auto_20210320_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncard',
            name='artist',
            field=models.CharField(default='ass', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='collectioncard',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]
