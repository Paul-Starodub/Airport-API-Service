# Generated by Django 4.2.6 on 2023-10-26 13:07

import airplanes.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("airplanes", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="airplane",
            name="image",
            field=models.ImageField(
                null=True, upload_to=airplanes.models.plane_image_file_path
            ),
        ),
    ]
