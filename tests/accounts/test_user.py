import pytest
from django.contrib.auth import get_user_model
from model_bakery import baker



UserModel = get_user_model()

@pytest.mark.django_db
def test_new_user_defaults_to_user_role():
    user = baker.make(UserModel)
    assert user.role == UserModel.Role.USER