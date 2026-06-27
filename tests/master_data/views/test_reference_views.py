import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker
from master_data.models import Profile, Workpiece, Reference



UserModel = get_user_model()


@pytest.mark.django_db
def test_reference_visible_under_correct_parent():
    profile_code = '15000'
    workpiece_material = '10000000'
    reference_material = '20000000'

    user = baker.make(
        UserModel,
        role=UserModel.Role.USER,
    )

    profile = baker.make(
        Profile,
        code=profile_code
    )

    workpiece = baker.make(
        Workpiece,
        material = workpiece_material,
        profile=profile
    )

    reference = baker.make(
        Reference,
        material=reference_material,
        workpiece=workpiece,
    )

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(f'/api/master-data/profiles/{profile_code}/workpieces/{workpiece_material}/references/{reference_material}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_reference_hidden_under_wrong_profile():
    correct_profile_code = '15000'
    wrong_profile_code = '16000'
    workpiece_material = '10000000'
    reference_material = '20000000'

    user = baker.make(
        UserModel,
        role=UserModel.Role.USER,
    )

    correct_profile = baker.make(
        Profile,
        code=correct_profile_code,
    )

    wrong_profile = baker.make(
        Profile,
        code=wrong_profile_code,
    )

    workpiece = baker.make(
        Workpiece,
        material = workpiece_material,
        profile=correct_profile
    )

    reference = baker.make(
        Reference,
        material=reference_material,
        workpiece=workpiece,
    )

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    response = client.get(f'/api/master-data/profiles/{wrong_profile_code}/workpieces/{workpiece_material}/references/{reference_material}/')

    assert response.status_code == 404


@pytest.mark.django_db
def test_create_reference_with_mismatched_profile_in_url_returns_404():
    correct_profile_code = '15000'
    wrong_profile_code = '16000'
    workpiece_material = '10000000'
    reference_material = '20000000'

    user = baker.make(
        UserModel,
        role=UserModel.Role.MODERATOR,
    )

    correct_profile = baker.make(
        Profile,
        code=correct_profile_code,
    )

    wrong_profile = baker.make(
        Profile,
        code=wrong_profile_code,
    )

    workpiece = baker.make(
        Workpiece,
        material = workpiece_material,
        profile=correct_profile
    )

    reference = baker.prepare(
        Reference,
        material=reference_material,
        workpiece=workpiece,
    )

    client = APIClient()
    client.force_authenticate(
        user=user
    )

    payload = {
        'workpiece': workpiece_material,
        'material': reference_material,
        'description': reference.description,
        'theoretical_weight': reference.theoretical_weight,
    }

    response = client.post(
        f'/api/master-data/profiles/{wrong_profile_code}/workpieces/{workpiece_material}/references/',
        data=payload,
        format='json',
    )

    assert response.status_code == 404
    assert Reference.objects.count() == 0
