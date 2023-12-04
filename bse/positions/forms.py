from django import forms

from bse.positions.models import Position


class AddSellPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price')
