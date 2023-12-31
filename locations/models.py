from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class Airport(models.Model):
    """Description of an airport"""

    name = models.CharField(max_length=128)
    closest_big_city = models.CharField(max_length=128)
    likes = models.ManyToManyField(
        get_user_model(), related_name="airports", blank=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
        unique_together = ("name", "closest_big_city")


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
        return f"Route #{self.id}"

    def clean(self) -> None:
        if self.source == self.destination:
            raise ValidationError("Source and destination cannot be the same")

    def save(self, *args: tuple, **kwargs: dict) -> None:
        self.clean()
        super().save(*args, **kwargs)
