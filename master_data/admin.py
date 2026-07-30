from django.contrib import admin
from master_data.models import Profile



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
