from decimal import Decimal
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker



UserModel = get_user_model()


@pytest.mark.django_db
def test_anon_can_list_profiles():
    client = APIClient()

    response = client.get('/api/master-data/profiles/')

    assert response.status_code == 401


@pytest.mark.django_db
def test_logged_user_can_list_profiles():
    user = baker.make(
        UserModel,
        role=UserModel.Role.USER)
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get('/api/master-data/profiles/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_moderator_can_create_profile():
    user = baker.make(
        UserModel,
        role=UserModel.Role.MODERATOR)
    client = APIClient()
    client.force_authenticate(user=user)
    payload = {
        'code': '51233',
        'description': 'DESCRIPTION',
        'theoretical_gpm': Decimal('1000.00'),
    }

    response = client.post('/api/master-data/profiles/', data=payload)

    assert response.status_code == 201


@pytest.mark.django_db
def test_user_cannot_create_profile():
    user = baker.make(
        UserModel,
        role=UserModel.Role.USER)
    client = APIClient()
    client.force_authenticate(user=user)
    payload = {
        'code': '51233',
        'description': 'DESCRIPTION',
        'theoretical_gpm': Decimal('1000.00'),
    }

    response = client.post('/api/master-data/profiles/', data=payload)

    assert response.status_code == 403
