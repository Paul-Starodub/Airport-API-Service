from rest_framework import serializers

from locations.models import Route, Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("source", "destination", "distance")


class RouteListSerializer(RouteDetailSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)
