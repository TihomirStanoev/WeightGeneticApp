from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal
from common.models import BaseModel, MaterialModel
from master_data.constants import ProfileValidationErrorMessages


class Profile(BaseModel):
    code = models.CharField(
        max_length=15,
        unique=True,
    )

    description = models.CharField(
        max_length=40,
    )

    theoretical_gpm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=Decimal('0.01'),
                message=ProfileValidationErrorMessages.THEORETICAL_GRM_MESSAGE)],
    )


    def __str__(self):
        return f'{self.code} - {self.description}'


class Workpiece(BaseModel, MaterialModel):
    profile = models.ForeignKey(
        to='Profile',
        on_delete=models.CASCADE,
        related_name='workpieces'
    )
    nominal_length_mm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=Decimal('0.01'),
                message=ProfileValidationErrorMessages.NOMINAL_LENGTH_MESSAGE)],
    )

    def __str__(self):
        return f'{self.material} - {self.description} - {self.nominal_length_mm} mm'


class Reference(BaseModel, MaterialModel):
    workpiece = models.ForeignKey(
        to='Workpiece',
        on_delete=models.CASCADE,
        related_name='references'
    )
    customer_number = models.CharField(
        max_length=40,
        blank=True,
        null=True
    )
