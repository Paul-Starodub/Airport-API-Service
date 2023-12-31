from datetime import timedelta
from typing import Optional, Any

from django.db import models

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
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crews = models.ManyToManyField(to=Crew, related_name="flights", blank=True)

    def __str__(self) -> str:
        return f"Flight #{self.id}"

    def get_time_trip_in_hours(self) -> int:
        # 900 km/h - speed of an airplane
        return round(self.route.distance / 900)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: Optional[Any] = None,
        update_fields: Optional[Any] = None,
    ) -> None:
        # take 3 hours for registration/leaving airport
        if not self.arrival_time:
            time_trip = self.get_time_trip_in_hours()
            self.arrival_time = self.departure_time + timedelta(
                hours=time_trip + 3
            )

        super(Flight, self).save(
            force_insert, force_update, using, update_fields
        )
