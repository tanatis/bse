from django.urls import path

from bse.core.views import index

urlpatterns = [
    path('', index, name='index')
]