# Generated by Django 3.2.6 on 2021-08-19 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nails', '0003_rename_nails_feedback'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='nails',
            new_name='feedback',
        ),
    ]