from decimal import Decimal
import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker
from master_data.models import Workpiece


@pytest.mark.django_db
@pytest.mark.parametrize(
    'invalid_length',
    [Decimal('0.00'), Decimal('-1.00')])
def test_nominal_length_below_minimum_raises(invalid_length):
    workpiece = baker.make(Workpiece, nominal_length_mm=invalid_length)
    with pytest.raises(ValidationError) as e:
        workpiece.full_clean()
    assert 'nominal_length_mm' in e.value.message_dict



@pytest.mark.django_db
def test_workpiece_str():
    material = '10000000'
    description = 'description'
    nominal_length_mm = Decimal('1000.00')

    workpiece = baker.make(
        Workpiece,
        material=material,
        description=description,
        nominal_length_mm=nominal_length_mm)

    assert  str(workpiece) == f'{material} - {description.upper()} - {nominal_length_mm} mm'

