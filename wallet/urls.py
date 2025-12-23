from django.urls import path
from . import views

urlpatterns = [
    path('balance/', views.WalletBalanceView.as_view(), name='wallet_balance'),
    path('credit/', views.WalletCreditView.as_view(), name='wallet_credit'),
    path('debit/', views.WalletDebitView.as_view(), name='wallet_debit'),
]