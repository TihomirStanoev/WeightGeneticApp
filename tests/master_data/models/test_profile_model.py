import pytest
from model_bakery import baker
from master_data.models import Profile



@pytest.mark.django_db
def test_profile_str():
    code = '123445'
    description = 'DESCRIPTION'

    profile = baker.make(
        Profile,
        code=code,
        description=description,
    )

    assert str(profile) == f'{code} - {description}'