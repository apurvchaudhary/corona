# Generated by Django 3.0.4 on 2020-04-07 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corona_app', '0009_delete_about'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='help_line_number',
            field=models.CharField(blank=True, default=104, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='state',
            name='help_line_number',
            field=models.CharField(blank=True, default=104, max_length=100, null=True),
        ),
    ]
