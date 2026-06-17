from rest_framework import serializers

from master_data.models import Profile, Workpiece, Reference


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'code',
            'description',
            'theoretical_gpm',
        )



class WorkpieceSerializer(serializers.ModelSerializer):
    profile = serializers.SlugRelatedField(
        read_only = True,
        slug_field = 'code'
    )

    class Meta:
        model = Workpiece
        fields = (
            'profile',
            'nominal_length_mm',
            'material',
            'description',
            'theoretical_weight',
        )


class ReferenceSerializer(serializers.ModelSerializer):
    workpiece = serializers.SlugRelatedField(
        read_only = True,
        slug_field='material',
    )

    class Meta:
        model = Reference
        fields = (
            'workpiece',
            'customer_number',
            'material',
            'description',
            'theoretical_weight',
        )