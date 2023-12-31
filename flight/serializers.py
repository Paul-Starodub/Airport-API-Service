from rest_framework import serializers

from airplanes.serializers import (
    AirplaneListSerializer,
    AirplaneDetailSerializer,
)
from flight.models import Crew, Flight
from locations.serializers import RouteDetailSerializer


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "flights")
        read_only_fields = ("flights",)


class CrewDetailSerializer(CrewSerializer):
    flights = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field="departure_time"
    )


class FlightSerializer(serializers.ModelSerializer):
    def validate_crews(self, crews: list[Crew]) -> list[Crew]:
        if len(crews) != len(set(crews)):
            raise serializers.ValidationError(
                "A crew member cannot be added more than once to a flight."
            )
        return crews

    class Meta:
        model = Flight
        fields = (
            "id",
            "airplane",
            "route",
            "departure_time",
            "crews",
        )


class FlightListSerializer(FlightSerializer):
    airplane = AirplaneListSerializer(many=False, read_only=True)
    crews = serializers.StringRelatedField(many=True, read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + (
            "arrival_time",
            "tickets_available",
        )


class FlightDetailSerializer(FlightSerializer):
    airplane = AirplaneDetailSerializer(many=False, read_only=True)
    crews = CrewSerializer(many=True, read_only=True)
    taken_rows_and_seats = serializers.SerializerMethodField()
    route = RouteDetailSerializer(many=False, read_only=True)

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ("taken_rows_and_seats",)

    def get_taken_rows_and_seats(self, obj: Flight) -> list[str]:
        taken_rows_and_seats = []

        for row, seat in zip(
            obj.tickets.values("row"), obj.tickets.values("seat")
        ):
            taken_rows_and_seats.append(f"{row}{seat}")
        return taken_rows_and_seats
