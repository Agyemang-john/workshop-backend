# Generated by Django 5.1.7 on 2025-03-15 13:58

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='speaker',
            name='profile_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='cover_image',
            field=cloudinary.models.CloudinaryField(blank=True, max_length=255, null=True, verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='workshop',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('disabled', 'Disabled'), ('published', 'Published')], default='draft', max_length=50),
        ),
    ]
