# Generated by Django 3.2.9 on 2022-02-28 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0015_auto_20220228_1714'),
    ]

    operations = [
        migrations.RenameField(
            model_name='building',
            old_name='location_name',
            new_name='loc_name',
        ),
    ]