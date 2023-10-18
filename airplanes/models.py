from django.db import models


class AirplaneType(models.Model):
    """Type of airplane"""

    name = models.CharField(max_length=63, unique=True)

    def __str__(self) -> str:
        return self.name


class Airplane(models.Model):
    """Airplane characteristics"""

    name = models.CharField(max_length=63)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()
    airplane_type = models.ForeignKey(
        to=AirplaneType, on_delete=models.CASCADE, related_name="airplanes"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
