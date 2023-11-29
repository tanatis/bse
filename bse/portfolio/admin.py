from django.contrib import admin

from bse.portfolio.models import Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass
