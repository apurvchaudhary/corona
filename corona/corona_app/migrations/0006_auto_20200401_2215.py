# Generated by Django 3.0.4 on 2020-04-01 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corona_app', '0005_auto_20200401_2142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
