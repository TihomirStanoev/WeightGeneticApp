from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker

from extrusion.models import Extrusion
from master_data.models import Reference, Profile, Workpiece
from measurements.models import Batch, Measurement

UserModel = get_user_model()



@pytest.mark.django_db
def test_measurement_visible_under_correct_parent():
    correct_reference = '10101010'
    card_no = '10000000'
    correct_profile_code = '15000'
    grm = Decimal('1000.00')
    length_mm = Decimal('2000.00')
    workpiece_weight_gr = Decimal('500.00')
    machined_weight_gr = Decimal('450.00')


    profile = baker.make(
        Profile,
        code = correct_profile_code,
        theoretical_gpm = grm,
    )

    extrusion = baker.make(
        Extrusion,
        profile = profile,
        card_no = card_no,
        card_grm = grm,
    )

    reference = baker.make(
        Reference,
        material = correct_reference,
        theoretical_weight=machined_weight_gr,
    )
    batch = baker.make(
        Batch,
        reference = reference,
    )
    measurement = baker.make(
        Measurement,
        batch = batch,
        card=extrusion,
        length_mm=length_mm,
        workpiece_weight_gr=workpiece_weight_gr,
    )


    user = baker.make(
        UserModel,
        role = UserModel.Role.USER,
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(f'/api/measurements/references/{correct_reference}/batches/{batch.pk}/measurements/{measurement.pk}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_measurement_hidden_under_wrong_parent():
    correct_reference = '10101010'
    wrong_reference = '10000000'
    card_no = '10000000'
    correct_profile_code = '15000'
    grm = Decimal('1000.00')
    length_mm = Decimal('2000.00')
    workpiece_weight_gr = Decimal('500.00')
    machined_weight_gr = Decimal('450.00')


    profile = baker.make(
        Profile,
        code = correct_profile_code,
        theoretical_gpm = grm,
    )

    extrusion = baker.make(
        Extrusion,
        profile = profile,
        card_no = card_no,
        card_grm = grm,
    )

    reference_a = baker.make(
        Reference,
        material = correct_reference,
        theoretical_weight=machined_weight_gr,
    )
    reference_b = baker.make(
        Reference,
        material = wrong_reference,
        theoretical_weight=machined_weight_gr,
    )


    correct_batch = baker.make(
        Batch,
        reference = reference_a,
    )

    wrong_batch = baker.make(
        Batch,
        reference = reference_b,
    )


    measurement = baker.make(
        Measurement,
        batch = correct_batch,
        card=extrusion,
        length_mm=length_mm,
        workpiece_weight_gr=workpiece_weight_gr,
    )


    user = baker.make(
        UserModel,
        role = UserModel.Role.USER,
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(f'/api/measurements/references/{correct_reference}/batches/{wrong_batch.pk}/measurements/{measurement.pk}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_measurement_hidden_under_wrong_reference():
    correct_reference = '10101010'
    wrong_reference = '10000000'
    card_no = '10000000'
    correct_profile_code = '15000'
    grm = Decimal('1000.00')
    length_mm = Decimal('2000.00')
    workpiece_weight_gr = Decimal('500.00')
    machined_weight_gr = Decimal('450.00')


    profile = baker.make(
        Profile,
        code = correct_profile_code,
        theoretical_gpm = grm,
    )

    extrusion = baker.make(
        Extrusion,
        profile = profile,
        card_no = card_no,
        card_grm = grm,
    )

    reference_a = baker.make(
        Reference,
        material = correct_reference,
        theoretical_weight=machined_weight_gr,
    )
    reference_b = baker.make(
        Reference,
        material = wrong_reference,
        theoretical_weight=machined_weight_gr,
    )

    correct_batch = baker.make(
        Batch,
        reference = reference_a,
    )

    measurement = baker.make(
        Measurement,
        batch = correct_batch,
        card=extrusion,
        length_mm=length_mm,
        workpiece_weight_gr=workpiece_weight_gr,
    )


    user = baker.make(
        UserModel,
        role = UserModel.Role.USER,
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(f'/api/measurements/references/{wrong_reference}/batches/{correct_batch.pk}/measurements/{measurement.pk}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_measurement_with_mismatched_reference_in_url_returns_404():
    correct_reference = '10101010'
    wrong_reference = '10000000'
    workpiece_material = '20202020'
    card_no = '10000000'
    correct_profile_code = '15000'
    grm = Decimal('1000.00')
    length_mm = Decimal('2000.00')
    workpiece_weight_gr = Decimal('500.00')
    machined_weight_gr = Decimal('450.00')


    profile = baker.make(
        Profile,
        code = correct_profile_code,
        theoretical_gpm = grm,
    )

    extrusion = baker.make(
        Extrusion,
        profile = profile,
        card_no = card_no,
        card_grm = grm,
    )

    workpiece = baker.make(
        Workpiece,
        profile = profile,
        material = workpiece_material,
        nominal_length_mm = length_mm,
        theoretical_weight = workpiece_weight_gr,
    )

    reference_a = baker.make(
        Reference,
        material = correct_reference,
        workpiece = workpiece,
        theoretical_weight=machined_weight_gr,
    )
    reference_b = baker.make(
        Reference,
        material = wrong_reference,
        workpiece = workpiece,
        theoretical_weight=machined_weight_gr,
    )

    correct_batch = baker.make(
        Batch,
        reference = reference_a,
    )


    moderator = baker.make(
        UserModel,
        role = UserModel.Role.MODERATOR,
    )

    payload = {
        'card': card_no,
        'length_mm': length_mm,
        'workpiece_weight_gr': workpiece_weight_gr,
    }

    client = APIClient()
    client.force_authenticate(user=moderator)
    response = client.post(
        f'/api/measurements/references/{wrong_reference}/batches/{correct_batch.pk}/measurements/',
        data=payload,
        format='json',
    )

    assert response.status_code == 404
    assert Measurement.objects.count() == 0
