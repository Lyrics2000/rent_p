# Generated by Django 3.2.9 on 2022-01-03 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_building_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True, help_text='The description of the room', null=True),
        ),
    ]