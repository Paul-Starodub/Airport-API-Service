from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from locations.models import Route, Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirportListSerializer(AirportSerializer):
    total_likes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city", "total_likes")


class AirportLikeSerializer(AirportSerializer):
    class Meta:
        model = Airport
        fields = ("id",)


class RouteSerializer(serializers.ModelSerializer):
    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs=attrs)
        source = attrs.get("source")
        destination = attrs.get("destination")

        if source == destination:
            raise ValidationError("Source and destination cannot be the same.")

        return data

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source = serializers.SlugRelatedField(
        slug_field="name", read_only=True, many=False
    )
    # written in another case just for practice
    destination = serializers.CharField(
        source="destination.name", read_only=True
    )


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)
