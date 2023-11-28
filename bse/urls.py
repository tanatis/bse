from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bse.account.urls')),
    path('', include('bse.tickers.urls')),
]
