from decimal import Decimal
import pytest
from model_bakery import baker
from master_data.models import Reference



@pytest.mark.django_db
def test_reference_str():
    material = '10000000'
    description = 'description'
    theoretical_weight = Decimal('2000.00')

    reference = baker.make(
        Reference,
        material=material,
        description=description,
        theoretical_weight=theoretical_weight)

    assert  str(reference) == f'{material} - {description.upper()} - {theoretical_weight} gr.'

