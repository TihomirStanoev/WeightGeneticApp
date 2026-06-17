from rest_framework import serializers

from extrusion.models import Extrusion


class ExtrusionSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'code'
    )

    class Meta:
        model = Extrusion
        fields = (
            'profile',
            'basket',
            'card_no',
            'card_grm',
            'k_route',
        )

        read_only_fields = (
            'k_route',
        )