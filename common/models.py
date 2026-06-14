from django.core.validators import RegexValidator, MinValueValidator
from django.db import models
from decimal import Decimal


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
        validators=[RegexValidator(r'^[12]\d{7}$', 'Please enter a valid material number.')]
    )
    description = models.CharField(
        max_length=40,
    )
    theoretical_weight = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'), 'Theoretical net weight must be greater than zero.')]
    )

    class Meta:
        abstract = True


    def __str__(self):
        return f'{self.material} - {self.description} - {self.theoretical_weight} gr.'


    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        super().save(*args, **kwargs)
