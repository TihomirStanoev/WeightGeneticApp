from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from extrusion.models import Extrusion
from master_data.models import Workpiece
from measurements.constants import MeasurementValidationErrorMessages
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



    def validate_length_mm(self, value):
        batch = self.context.get('batch')
        nominal_length_mm = batch.reference.workpiece.nominal_length_mm
        low = nominal_length_mm - Workpiece.LENGTH_TOLERANCE_MM
        high = nominal_length_mm + Workpiece.LENGTH_TOLERANCE_MM

        if low > value or value > high:
            raise ValidationError(MeasurementValidationErrorMessages.LENGTH_OUT_OF_RANGE.format(length=value, low=low, high=high))

        return value