import pytest
from decimal import Decimal
from model_bakery import baker
from master_data.models import Profile, Reference, Workpiece
from measurements.models import Batch
from extrusion.models import Extrusion
from measurements.serializers import MeasurementSerializer


@pytest.mark.django_db
def test_length_within_tolerance_is_valid():
    nominal = 1000
    measure = 1001
    nominal_length = Decimal(f'{nominal}')
    measure_length = Decimal(f'{measure}')

    profile = baker.make(
        Profile,
        code='15000',
        theoretical_gpm=Decimal('1000.00'),
    )
    workpiece = baker.make(
        Workpiece,
        profile=profile,
        nominal_length_mm=nominal_length,
        material='10000000',
    )
    reference = baker.make(
        Reference,
        workpiece=workpiece,
        material='10000001',
    )
    batch = baker.make(
        Batch,
        reference=reference,
    )
    card = baker.make(
        Extrusion,
        profile=profile,
        card_no='10101010',
        card_grm=Decimal('1000.00'),
    )
    data = {
        'card': card.card_no,
        'length_mm': measure_length,
        'workpiece_weight_gr': Decimal('1000.00'),
    }
    serializer = MeasurementSerializer(data=data, context={'batch': batch})

    assert serializer.is_valid(), serializer.errors


@pytest.mark.django_db
def test_length_below_tolerance_is_invalid():
    nominal = 1000
    measure = nominal - (Workpiece.LENGTH_TOLERANCE_MM + 1)
    nominal_length = Decimal(f'{nominal}')
    measure_length = Decimal(f'{measure}')

    profile = baker.make(
        Profile,
        code='15000',
        theoretical_gpm=Decimal('1000.00'),
    )
    workpiece = baker.make(
        Workpiece,
        profile=profile,
        nominal_length_mm=nominal_length,
        material='10000000',
    )
    reference = baker.make(
        Reference,
        workpiece=workpiece,
        material='10000001',
    )
    batch = baker.make(
        Batch,
        reference=reference,
    )
    card = baker.make(
        Extrusion,
        profile=profile,
        card_no='10101010',
        card_grm=Decimal('1000.00'),
    )
    data = {
        'card': card.card_no,
        'length_mm': measure_length,
        'workpiece_weight_gr': Decimal('1000.00'),
    }
    serializer = MeasurementSerializer(data=data, context={'batch': batch})

    assert not serializer.is_valid()
    assert 'length_mm' in serializer.errors


@pytest.mark.django_db
def test_length_above_tolerance_is_invalid():
    nominal = 1000
    measure = nominal + (Workpiece.LENGTH_TOLERANCE_MM + 1)
    nominal_length = Decimal(f'{nominal}')
    measure_length = Decimal(f'{measure}')

    profile = baker.make(
        Profile,
        code='15000',
        theoretical_gpm=Decimal('1000.00'),
    )
    workpiece = baker.make(
        Workpiece,
        profile=profile,
        nominal_length_mm=nominal_length,
        material='10000000',
    )
    reference = baker.make(
        Reference,
        workpiece=workpiece,
        material='10000001',
    )
    batch = baker.make(
        Batch,
        reference=reference,
    )
    card = baker.make(
        Extrusion,
        profile=profile,
        card_no='10101010',
        card_grm=Decimal('1000.00'),
    )
    data = {
        'card': card.card_no,
        'length_mm': measure_length,
        'workpiece_weight_gr': Decimal('1000.00'),
    }
    serializer = MeasurementSerializer(data=data, context={'batch': batch})

    assert not serializer.is_valid()
    assert 'length_mm' in serializer.errors
