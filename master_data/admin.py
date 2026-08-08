from django.contrib import admin
from master_data.models import Profile, Workpiece, Reference


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'description',
        'theoretical_gpm',
    )

    search_fields = (
        'code',
        'description',
    )


@admin.register(Workpiece)
class WorkpieceAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'material',
        'description',
        'nominal_length_mm',
        'theoretical_weight',
    )

    search_fields = (
        'profile__code',
        'material',
        'description',
    )


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = (
        'material',
        'description',
        'theoretical_weight',
        'customer_number',
        'workpiece',
    )

    search_fields = (
        'material',
        'description',
    )