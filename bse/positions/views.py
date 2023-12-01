from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

from bse.portfolio.models import Portfolio
from bse.positions.models import Position
from bse.tickers.models import Ticker


class CreatePositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ('count', 'price', 'to_portfolio')

    user = None  # Add a user field

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove user from kwargs and store it
        super().__init__(*args, **kwargs)

        if user:
            self.user = user
            self.fields['to_portfolio'].queryset = Portfolio.objects.filter(user=user)


@login_required(login_url='user_login')
def create_position(request, symbol):

    ticker = get_object_or_404(Ticker, symbol=symbol)
    portfolio = Portfolio.objects.filter(user=request.user)

    if not portfolio:
        messages.error(request, 'You must have at least one portfolio!')
        return redirect('portfolio_create')

    if request.method == 'POST':
        form = CreatePositionForm(request.POST, user=request.user)
        if form.is_valid():
            count = form.cleaned_data['count']
            price = form.cleaned_data['price']
            portfolio_id = form.cleaned_data['to_portfolio'].id
            portfolio = Portfolio.objects.get(pk=portfolio_id)
            if portfolio.cash < count * price:
                messages.error(request, 'no cash')
                return redirect(request.META['HTTP_REFERER'])

            existing_position = Position.objects.filter(ticker=ticker, to_portfolio_id=portfolio_id).first()

            if existing_position:
                existing_position.count += count
                existing_position.price += count * price
                existing_position.avg_price = existing_position.price / existing_position.count
                existing_position.save()
            else:
                # Create a new position
                position = Position(
                    ticker=ticker,
                    count=count,
                    price=price * count,
                    to_portfolio_id=portfolio_id,
                    avg_price=price,
                )
                position.save()
            portfolio.cash -= count * price
            portfolio.save()
            return redirect('portfolio_details', pk=portfolio.pk)

    else:
        form = CreatePositionForm(user=request.user)

    context = {
        'form': form,
        'ticker': ticker,
    }

    return render(request, 'positions/position-create.html', context)
