from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from common.models import BaseModel
from measurements.constants import MeasurementValidationErrorMessages


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

    def _calc_measured_gpm(self):
        if self.length_mm and self.length_mm > 0:
            return self.workpiece_weight_gr / (self.length_mm / 1000)
        return None


    def _calc_blank_theoretical(self):
        if self.length_mm and self.length_mm > 0:
            return self.card.profile.theoretical_gpm * (self.length_mm / 1000)
        return None

    def _calc_k_vs_basket(self, measured_gpm):
        if measured_gpm and self.card.card_grm > 0:
            return measured_gpm / self.card.card_grm
        return None


    def _calc_k_vs_theoretical(self, measured_gpm):
        if measured_gpm and self.card.profile.theoretical_gpm > 0:
            return measured_gpm / self.card.profile.theoretical_gpm
        return None


    def _calc_workpiece_delta_pct(self, blank_theoretical):
        if blank_theoretical:
            return (self.workpiece_weight_gr - blank_theoretical) / blank_theoretical * 100
        return None


    def _calc_reference_delta_pct(self, k_vs_theoretical):
        if self.machined_weight_gr and k_vs_theoretical and k_vs_theoretical > 0 and self.batch.reference.theoretical_weight > 0:
            predicted_net = self.batch.reference.theoretical_weight * k_vs_theoretical
            return (self.machined_weight_gr - predicted_net) / predicted_net * 100
        return None



    def save(self, *args, **kwargs):
        measured_gpm = self._calc_measured_gpm()
        k_vs_theoretical = self._calc_k_vs_theoretical(measured_gpm)
        blank_theoretical = self._calc_blank_theoretical()
        self.measured_gpm = measured_gpm
        self.k_vs_theoretical = k_vs_theoretical

        self.k_vs_basket = self._calc_k_vs_basket(measured_gpm)
        self.workpiece_delta_pct = self._calc_workpiece_delta_pct(blank_theoretical)
        self.reference_delta_pct = self._calc_reference_delta_pct(k_vs_theoretical)


        super().save(*args, **kwargs)



