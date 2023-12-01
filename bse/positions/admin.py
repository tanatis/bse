from django.contrib import admin

from bse.positions.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    pass
