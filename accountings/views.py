from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView

from .forms import TransactionForm
from .models import Accounts

# Create your views here.
def accounts(request):
    if request.user.is_authenticated:
        acc = Accounts.objects.filter(dept_name = request.user.dept_name)
    
    else:
        acc = Accounts.objects.all().order_by('dept_name')
    return render(request, 'accounts/accounts.html', {'accounts': acc})

class AccountCreate(CreateView):

    model = Accounts
    form_class = TransactionForm
    template_name = 'accounts/addaccount.html'

    def form_valid(self, form):
        
        try:

            if form.cleaned_data['transaction_type'] == 'D' and Accounts.objects.filter(dept_name = form.cleaned_data['dept_name']).last().current_balance - form.cleaned_data['amount'] < 0:
                messages.error(self.request, "Debit amount is more than what is available in department funds!")
                return render(self.request, self.template_name, {'form': form})
            
        except Exception: 
            if form.cleaned_data['transaction_type'] == 'D':
                messages.error(self.request, "Debit amount is more than what is available in department funds!")
                return render(self.request, self.template_name, {'form': form})

        account = form.save()

        if account:
            messages.success(self.request, f'Transaction from {account.transactee} recorded successfully!')
            return redirect('allaccounts')
        
    def form_invalid(self, form):

        return render(self.request, self.template_name, {'form': form})

