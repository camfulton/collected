# Generated by Django 3.1.7 on 2021-03-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0008_auto_20210320_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='collectioncard',
            name='name',
            field=models.CharField(default='ass', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collectioncard',
            name='number',
            field=models.CharField(default='0', max_length=25),
        ),
        migrations.AddField(
            model_name='collectioncard',
            name='set_name',
            field=models.CharField(default='ass', max_length=100),
            preserve_default=False,
        ),
    ]
