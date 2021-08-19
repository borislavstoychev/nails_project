# Generated by Django 3.2.6 on 2021-08-18 09:36

import cloudinary.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Nails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Pedicure', 'Pedicure'), ('Manicure', 'Manicure')], default='Manicure', max_length=10)),
                ('feedback', models.CharField(choices=[('Positive', 'Positive'), ('Negative', 'Negative')], default='Positive', max_length=10)),
                ('description', models.TextField()),
                ('image', cloudinary.models.CloudinaryField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nails', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nails.nails')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]