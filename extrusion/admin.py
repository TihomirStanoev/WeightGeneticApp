from django.contrib import admin
from extrusion.models import Extrusion


@admin.register(Extrusion)
class ExtrusionAdmin(admin.ModelAdmin):
    list_display = (
        'profile',
        'basket',
        'card_no',
        'card_grm',
        'k_route',
    )

    search_fields = (
        'profile__code',
        'card_no',
    )