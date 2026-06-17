from rest_framework import serializers

from extrusion.models import Extrusion
from measurements.models import Batch, Measurement


class BatchSerializer(serializers.ModelSerializer):
    reference = serializers.SlugRelatedField(
        slug_field='material',
        read_only=True,
    )

    class Meta:
        model = Batch
        fields = (
            'reference',
            'date',
            'status',
        )



class MeasurementSerializer(serializers.ModelSerializer):
    batch = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    card = serializers.SlugRelatedField(
        slug_field='card_no',
        queryset=Extrusion.objects.all()
    )

    class Meta:
        model = Measurement
        read_only_fields = (
            'measured_gpm',
            'k_vs_basket',
            'k_vs_theoretical',
            'workpiece_delta_pct',
            'reference_delta_pct',
        )

        fields = (
            'batch',
            'card',
            'length_mm',
            'workpiece_weight_gr',
            'machined_weight_gr',
        ) + read_only_fields

