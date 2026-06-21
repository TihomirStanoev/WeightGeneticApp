import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker
from master_data.models import Profile, Workpiece


UserModel = get_user_model()


@pytest.mark.django_db
def test_workpiece_visible_under_correct_parent():
    material = '10000000'
    parent_code = '23000'
    profile_a = baker.make(
        Profile,
        code=parent_code,
    )
    workpiece = baker.make(
        Workpiece,
        profile = profile_a,
        material = material,
    )
    user = baker.make(
        UserModel,
        role = UserModel.Role.USER,
    )
    client = APIClient()

    client.force_authenticate(
        user=user
    )

    response = client.get(f'/api/master-data/profiles/{parent_code}/workpieces/{material}/')

    assert response.status_code == 200



@pytest.mark.django_db
def test_workpiece_hidden_under_wrong_parent():
    material = '10000001'
    parent_code = '20000'
    wrong_parent_code = '25000'

    profile_a = baker.make(
        Profile,
        code=parent_code,
    )
    profile_b = baker.make(
        Profile,
        code=wrong_parent_code,
    )
    workpiece = baker.make(
        Workpiece,
        profile=profile_a,
        material=material
    )

    user = baker.make(
        UserModel,
        role=UserModel.Role.USER
    )

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get(f'/api/master-data/profiles/{wrong_parent_code}/workpieces/{material}/')

    assert response.status_code == 404