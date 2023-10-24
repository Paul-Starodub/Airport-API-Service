from rest_framework import serializers

from airplanes.serializers import (
    AirplaneListSerializer,
    AirplaneDetailSerializer,
)
from flight.models import Crew, Flight
from locations.serializers import RouteListSerializer, RouteDetailSerializer


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
            "route",
            "airplane",
            "departure_time",
            "crews",
        )


class FlightListSerializer(FlightSerializer):
    airplane = AirplaneListSerializer(many=False, read_only=True)
    route = RouteListSerializer(many=False, read_only=True)
    crews = serializers.StringRelatedField(many=True, read_only=True)

    class Meta(FlightSerializer.Meta):
        fields = FlightSerializer.Meta.fields + ("arrival_time",)


class FlightDetailSerializer(FlightListSerializer):
    airplane = AirplaneDetailSerializer(many=False, read_only=True)
    route = RouteDetailSerializer(many=False, read_only=True)
    crews = CrewSerializer(many=True, read_only=True)
