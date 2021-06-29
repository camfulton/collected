# Generated by Django 3.1.7 on 2021-03-19 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='english',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='foil',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='french',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='german',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='italian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='japanese',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='korean',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='nonfoil',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='collection',
            name='portuguese',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='russian',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='s_chinese',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='spanish',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collection',
            name='t_chinese',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='collectioncard',
            name='foil',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='collectioncard',
            name='language',
            field=models.CharField(default='English', max_length=50),
            preserve_default=False,
        ),
    ]
