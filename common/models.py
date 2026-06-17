from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from decimal import Decimal

from common.constants import MaterialModelValidationErrorMessages


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        abstract = True



class MaterialModel(models.Model):
    material = models.CharField(
        max_length=8,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[12]\d{7}$',
                message=MaterialModelValidationErrorMessages.VALID_MATERIAL_MESSAGE)
        ]
    )

    description = models.CharField(
        max_length=40,
    )
    theoretical_weight = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal('0.01'),
                message=MaterialModelValidationErrorMessages.THEORETICAL_NET_MESSAGE)]
    )

    class Meta:
        abstract = True


    def __str__(self):
        return f'{self.material} - {self.description} - {self.theoretical_weight} gr.'


    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        super().save(*args, **kwargs)
