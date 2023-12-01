from django.urls import path

from bse.portfolio.views import PortfolioDetailsView, PortfolioCreateView, PortfolioDeleteView, cash_operations

urlpatterns = [
    path('portfolio/<int:pk>/', PortfolioDetailsView.as_view(), name='portfolio_details'),
    path('portfolio/create/', PortfolioCreateView.as_view(), name='portfolio_create'),
    path('portfolio/<int:pk>/delete/', PortfolioDeleteView.as_view(), name='portfolio_delete'),
    path('portfolio/<int:pk>/cash/', cash_operations, name='portfolio_cash'),
]
