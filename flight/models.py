from django.db import models
from django.core.exceptions import ValidationError

from airplanes.models import Airplane
from locations.models import Route


class Crew(models.Model):
    """Description of a crew"""

    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    def __str__(self) -> str:
        return f"Person: {self.first_name} {self.last_name}"

    class Meta:
        ordering = ("last_name",)


class Flight(models.Model):
    """Everything about a flight"""

    route = models.ForeignKey(
        to=Route, on_delete=models.CASCADE, related_name="flying"
    )
    airplane = models.ForeignKey(
        to=Airplane, on_delete=models.CASCADE, related_name="flying"
    )
    departure_time = models.DateTimeField(auto_now_add=True)
    arrival_time = models.DateTimeField(auto_now_add=True)
    crews = models.ManyToManyField(to=Crew, related_name="flights")

    def __str__(self) -> str:
        return f"Route #{self.id}"

    def clean(self) -> None:
        if self.arrival_time <= self.departure_time:
            raise ValidationError(
                "Arrival time must be greater than departure time."
            )
