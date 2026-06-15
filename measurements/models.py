from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from common.models import BaseModel
from extrusion.constants import MeasurementValidationErrorMessages


class Batch(BaseModel):
    class StatusChoice(models.TextChoices):
        PLANNED = 'planned', 'planned'
        DRAFT = 'draft', 'draft'
        COMPLETE = 'complete', 'complete'

    reference = models.ForeignKey(
        to='master_data.Reference',
        related_name='batches',
        on_delete=models.CASCADE,
    )

    date = models.DateField()

    status = models.CharField(
        max_length=15,
        choices=StatusChoice.choices,
        default=StatusChoice.DRAFT,
    )

    class Meta:
        ordering = ['-date', 'status']

    def __str__(self):
        return f'{self.reference} / {self.date} - {self.status}'



class Measurement(BaseModel):
    batch = models.ForeignKey(
        to='Batch',
        related_name='measurements',
        on_delete=models.CASCADE
    )

    card = models.ForeignKey(
        to='extrusion.Extrusion',
        related_name='measurements',
        on_delete=models.CASCADE,
    )

    length_mm = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=Decimal('0.01'),
                message=MeasurementValidationErrorMessages.LENGTH_MM_MESSAGE)
        ]
    )

    workpiece_weight_gr = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=Decimal('0.01'),
                message=MeasurementValidationErrorMessages.WEIGHT_GR_MESSAGE)]
    )

    machined_weight_gr = models.DecimalField(
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=2,
        validators=[
            MinValueValidator(
                limit_value=Decimal('0.01'),
                message=MeasurementValidationErrorMessages.WEIGHT_GR_MESSAGE)]
    )

    measured_gpm = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        editable=False,
        null=True,
        blank=True
    )

    k_vs_basket = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        editable=False,
        blank=True,
        null=True
    )

    k_vs_theoretical = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        editable=False,
        blank=True,
        null=True
    )

    workpiece_delta_pct = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        editable=False,
        blank=True,
        null=True
    )

    reference_delta_pct = models.DecimalField(
        max_digits=6,
        decimal_places=4,
        editable=False,
        blank=True,
        null=True
    )

    @property
    def blank_theoretical(self):
        return self.batch.reference.workpiece.profile.theoretical_gpm * (self.length_mm / 1000)



    def save(self, *args, **kwargs):
        self.measured_gpm = self.workpiece_weight_gr / (self.length_mm / 1000)
        self.k_vs_basket = self.measured_gpm / self.card.card_grm
        self.k_vs_theoretical = self.measured_gpm / self.card.profile.theoretical_gpm
        self.workpiece_delta_pct = (self.workpiece_weight_gr - self.blank_theoretical) / self.blank_theoretical * 100

        if self.machined_weight_gr is not None:
            predicted_net = self.batch.reference.theoretical_weight * self.k_vs_theoretical
            self.reference_delta_pct = (self.machined_weight_gr - predicted_net) / predicted_net * 100


        super().save(*args, **kwargs)



