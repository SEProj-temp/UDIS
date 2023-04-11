from django.urls import path
from . import views

urlpatterns = [
    
    path('accounts/', views.accounts, name = 'allaccounts'),
    path('accounts/addaccount/', views.AccountCreate.as_view(), name = 'addacc'),
]