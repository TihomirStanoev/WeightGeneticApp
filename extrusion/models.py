from decimal import Decimal
from django.core.validators import RegexValidator, MinValueValidator
from django.db import models

from common.models import BaseModel
from extrusion.constants import ExtrusionValidationErrorMessages


class Extrusion(BaseModel):
    profile = models.ForeignKey(
        to='master_data.Profile',
        on_delete=models.CASCADE,
        related_name='cards'
    )

    basket = models.CharField(
        max_length=4,
        validators=[
            RegexValidator(
                regex=r'^\d{,4}$',
                message=ExtrusionValidationErrorMessages.INVALID_BASKET_MESSAGE)]
    )

    card_no = models.CharField(
        max_length=8,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message=ExtrusionValidationErrorMessages.INVALID_CARD_MESSAGE)]
    )

    card_grm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(
            Decimal('0.01'),
            message=ExtrusionValidationErrorMessages.GRM_MESSAGE)]
    )

    k_route = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        editable=False,
        blank=True,
        null=True
    )


    def __str__(self):
        return f'{self.profile} - {self.basket} - {self.card_no}'


    def save(self, *args, **kwargs):
        self.k_route = self.card_grm / self.profile.theoretical_gpm
        super().save(*args, **kwargs)

