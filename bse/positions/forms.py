from django import forms

from bse.portfolio.models import Portfolio
from bse.positions.models import Position


class AddSellPositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price', 'date_added')
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date'})
        }


class CreatePositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price', 'date_added', 'to_portfolio')
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date'})
        }

    user = None  # Add a user field

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove user from kwargs and store it
        super().__init__(*args, **kwargs)

        if user:
            self.user = user
            self.fields['to_portfolio'].queryset = Portfolio.objects.filter(user=user)
