from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from bse.portfolio.models import Portfolio
from bse.positions.forms import AddSellPositionForm
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


def is_portfolio_user(user, portfolio):
    return user == portfolio.user


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


@login_required(login_url='user_login')
def add_to_position(request, pk):
    position = Position.objects.filter(pk=pk).get()
    portfolio = Portfolio.objects.filter(pk=position.to_portfolio_id).get()
    if portfolio.user != request.user:
        raise Http404()

    if request.method == 'GET':
        form = AddSellPositionForm()
    else:
        form = AddSellPositionForm(request.POST)
        if form.is_valid():
            price_per_share = form.cleaned_data['price']
            count = form.cleaned_data['count']
            if count * price_per_share > portfolio.cash:
                messages.error(request, "Not enough cash to complete the operation")
                return redirect('portfolio_details', pk=portfolio.pk)

            position.count += count
            position.price += count * price_per_share
            position.avg_price = position.price / position.count
            position.save()

            portfolio.cash -= count * price_per_share
            portfolio.save()

            return redirect('portfolio_details', pk=portfolio.pk)

    context = {
        'form': form,
        'position': position,
        'portfolio': portfolio,
    }
    return render(request, 'positions/position_add.html', context)


@login_required(login_url='user_login')
def sell_position(request, pk):
    position = Position.objects.get(pk=pk)
    portfolio = Portfolio.objects.filter(pk=position.to_portfolio_id).get()

    if portfolio.user != request.user:
        raise Http404()

    if request.method == 'GET':
        form = AddSellPositionForm()
    else:
        form = AddSellPositionForm(request.POST)
        if form.is_valid():
            count = form.cleaned_data['count']
            price_per_share = form.cleaned_data['price']
            if count > position.count:
                messages.error(request, f"You cannot sell more than {position.count} shares")
                return redirect('portfolio_details', pk=portfolio.pk)
            elif count == position.count:
                position.delete()
            else:
                position.count -= count
                position.price -= count * position.avg_price
                position.save()

            portfolio.cash += count * price_per_share
            portfolio.save()

            return redirect('portfolio_details', pk=portfolio.pk)

    context = {
        'form': form,
        'position': position,
        'portfolio': portfolio,
    }
    return render(request, 'positions/position_sell.html', context)
