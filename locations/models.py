from django.db import models
from django.core.exceptions import ValidationError


class Airport(models.Model):
    """Description of an airport"""

    name = models.CharField(max_length=128, unique=True)
    closest_big_city = models.CharField(max_length=128)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)


class Route(models.Model):
    """All the information about trip"""

    source = models.ForeignKey(
        to=Airport, on_delete=models.CASCADE, related_name="first_routes"
    )
    destination = models.ForeignKey(
        to=Airport, on_delete=models.CASCADE, related_name="last_routes"
    )
    distance = models.PositiveBigIntegerField()

    def __str__(self) -> str:
        return f"Route from {self.source} to {self.destination}"

    def clean(self) -> None:
        if self.source == self.destination:
            raise ValidationError("Source and destination cannot be the same")

    def save(self, *args, **kwargs) -> None:
        self.clean()
        super().save(*args, **kwargs)
