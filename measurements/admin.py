from django.contrib import admin

from measurements.models import Batch, Measurement



class MeasurementTabularInline(admin.TabularInline):
    model = Measurement
    extra = 1
    min_num = 0


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'reference',
        'date',
        'status',
    )

    inlines = (
        MeasurementTabularInline,
    )



@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = (
        'batch',
        'card',
        'length_mm',
        'workpiece_weight_gr',
        'machined_weight_gr',
        'measured_gpm',

        'k_vs_basket',
        'k_vs_theoretical',
        'reference_delta_pct',
    )

    readonly_fields = (
        'k_vs_basket',
        'k_vs_theoretical',
        'reference_delta_pct',
    )
