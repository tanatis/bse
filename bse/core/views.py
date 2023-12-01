from django.db.models import Q
from django.shortcuts import render
from django import forms

from bse.tickers.models import Ticker


class SearchTickerForm(forms.Form):
    query = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search stocks ...',
                'class': '',
            }
        )
    )


def index(request):
    all_tickers = Ticker.objects.all()
    search_result = None
    form = SearchTickerForm(request.GET)
    search_pattern = None

    if form.is_valid():
        search_pattern = form.cleaned_data['query']

    if search_pattern:
        search_result = all_tickers.filter(
            Q(symbol__icontains=search_pattern) | Q(company_name__icontains=search_pattern)
        )

    context = {
        'search_result': search_result,
        'form': form,
    }

    return render(request, 'index.html', context)
