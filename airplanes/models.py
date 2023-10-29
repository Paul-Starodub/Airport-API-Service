from __future__ import annotations
import os
import uuid

from django.db import models
from django.utils.text import slugify


class AirplaneType(models.Model):
    """Type of airplane"""

    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


def plane_image_file_path(instance: Airplane, filename: str) -> str:
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"
    return os.path.join("uploads/planes/", filename)


class Airplane(models.Model):
    """Airplane characteristics"""

    name = models.CharField(max_length=63)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    image = models.ImageField(null=True, upload_to=plane_image_file_path)
    airplane_type = models.ForeignKey(
        to=AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self) -> str:
        return self.name

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    class Meta:
        ordering = ("name",)
