from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, CreateView, DeleteView

from bse.portfolio.models import Portfolio
from bse.positions.models import Position, PositionHistory


class PortfolioDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Portfolio
    template_name = 'portfolio/portfolio-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        positions = Position.objects.filter(to_portfolio_id=self.object.pk)
        positions_value = 0
        for position in positions:
            position.history = PositionHistory.objects.filter(to_position=position)
            position.value = position.count * position.avg_price
            positions_value += position.value
        portfolio = self.get_object()
        portfolio.cash = portfolio.cash
        total = portfolio.cash + positions_value
        portfolio.cash_percentage = portfolio.cash / total * 100

        for position in positions:
            position.percentage = position.value / total * 100
        context['positions'] = positions
        context['total'] = total
        context['cash_percentage'] = portfolio.cash_percentage

        return context

    def test_func(self):
        portfolio = self.get_object()
        return self.request.user == portfolio.user

    '''
    The `get_object` method is overridden to use get_object_or_404.
    This ensures that if the requested portfolio does not exist,
    a 404 error will be raised, providing better security.
    '''

    def get_object(self, queryset=None):
        return get_object_or_404(Portfolio, pk=self.kwargs['pk'])

    '''
    This will result in a 404 response instead of a 403
    when the conditions specified in test_func are not met.
    '''

    def handle_no_permission(self):
        # Customize the 403 response to raise a 404 instead
        raise Http404("Portfolio not found")


class PortfolioCreateView(LoginRequiredMixin, CreateView):
    model = Portfolio
    template_name = 'portfolio/portfolio-create.html'
    fields = ('name', 'cash',)
    login_url = 'user_login'

    def form_valid(self, form):
        form.instance.user = self.request.user
        result = super().form_valid(form)
        return result

    def get_success_url(self, **kwargs):
        return reverse_lazy('portfolio_details', kwargs={'pk': self.object.pk})


class PortfolioDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Portfolio
    template_name = 'portfolio/portfolio-delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        portfolio = self.get_object()
        return self.request.user == portfolio.user

    def get_object(self, queryset=None):
        return get_object_or_404(Portfolio, pk=self.kwargs['pk'])

    def handle_no_permission(self):
        raise Http404


def cash_operations(request, pk):
    portfolio = Portfolio.objects.filter(pk=pk, user_id=request.user.id).get()

    if request.method == 'POST':
        operation = request.POST.get('operation')
        amount = float(request.POST.get('amount'))

        if amount > portfolio.cash or amount <= 0:
            messages.error(request, f'Error! Please fix the amount and try again!')
            return redirect(request.META['HTTP_REFERER'])

        if operation == 'deposit':
            portfolio.cash += amount
        elif operation == 'withdraw':
            portfolio.cash -= amount

        portfolio.save()
    return HttpResponseRedirect(reverse('portfolio_details', args=[pk]))
