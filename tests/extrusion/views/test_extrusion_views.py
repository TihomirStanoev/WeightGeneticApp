from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker
from master_data.models import Profile
from extrusion.models import Extrusion


UserModel = get_user_model()



@pytest.mark.django_db
def test_extrusion_visible_under_correct_parent():
    card_no = '10000000'
    profile_code = '15000'
    grm = Decimal('1000.00')

    profile = baker.make(
        Profile,
        code = profile_code,
        theoretical_gpm = grm,
    )

    extrusion = baker.make(
        Extrusion,
        profile = profile,
        card_no = card_no,
        card_grm = grm,
    )

    user = baker.make(
        UserModel,
        role=UserModel.Role.USER
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(f'/api/extrusion/{profile_code}/{card_no}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_extrusion_hidden_under_wrong_parent():
    card_no = '10000000'
    correct_profile_code = '15000'
    wrong_profile_code = '12000'
    grm = Decimal('1000.00')

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

    user = baker.make(
        UserModel,
        role=UserModel.Role.USER
    )

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(f'/api/extrusion/{wrong_profile_code}/{card_no}/')

    assert response.status_code == 404