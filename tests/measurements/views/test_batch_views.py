import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from model_bakery import baker
from master_data.models import Reference
from measurements.models import Batch



UserModel = get_user_model()


@pytest.mark.django_db
def test_batch_visible_under_correct_parent():
    correct_reference = '10101010'

    reference = baker.make(
        Reference,
        material = correct_reference,
    )

    batch = baker.make(
        Batch,
        reference = reference,
    )

    user = baker.make(
        UserModel,
        role = UserModel.Role.USER,
    )

    client = APIClient()
    client.force_authenticate(user = user)
    response = client.get(f'/api/measurements/references/{correct_reference}/batches/{batch.pk}/')

    assert response.status_code == 200


@pytest.mark.django_db
def test_batch_hidden_under_wrong_parent():
    correct_reference = '10101010'
    wrong_reference = '11111111'

    reference = baker.make(
        Reference,
        material = correct_reference,
    )

    batch = baker.make(
        Batch,
        reference = reference,
    )

    user = baker.make(
        UserModel,
        role = UserModel.Role.USER,
    )

    client = APIClient()
    client.force_authenticate(user = user)
    response = client.get(f'/api/measurements/references/{wrong_reference}/batches/{batch.pk}/')

    assert response.status_code == 404