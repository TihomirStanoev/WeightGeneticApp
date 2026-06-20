import pytest
from django.core.exceptions import ValidationError
from model_bakery import baker
from master_data.models import Workpiece
from django.db import IntegrityError


@pytest.mark.django_db
def test_description_is_uppercased_on_save():
    description = 'description field'
    workpiece = baker.make(Workpiece, description=description)
    assert workpiece.description == description.upper()


@pytest.mark.django_db
@pytest.mark.parametrize(
    'invalid_material',
    ['31234567', 'abcdefgh', '1e223454', '12312', '1233134'])
def test_invalid_material_raises_validation_error(invalid_material):
    workpiece = baker.make(Workpiece, material=invalid_material)
    with pytest.raises(ValidationError) as e:
        workpiece.full_clean()
    assert 'material' in e.value.message_dict



@pytest.mark.django_db
@pytest.mark.parametrize(
    'valid_material',
    ['10000000', '20000000']
)
def test_valid_material_passes_validation(valid_material):
    workpiece = baker.make(Workpiece, material=valid_material)
    workpiece.full_clean()



@pytest.mark.django_db
def test_material_must_be_unique():
    material = '10000000'
    baker.make(Workpiece, material=material)
    with pytest.raises(IntegrityError):
        baker.make(Workpiece, material=material)