from django import forms
from .models import Accounts

class TransactionForm(forms.ModelForm):

    amount = forms.IntegerField(min_value = 0, required = True, widget=forms.TextInput(attrs={'placeholder': 'Transaction amount (in Rs)'}))
    dept_name = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'}))
    transaction_type = forms.ChoiceField(required = True, choices = Accounts.TYPE_CHOICES)
    transactee = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Transactee name'}))
    purpose = forms.CharField(required = True, max_length = 500, widget=forms.TextInput(attrs={'placeholder': 'Please enter the purpose'}))
    date_of_transaction = forms.DateField(required = True)
    current_balance = forms.IntegerField(required = False)

    class Meta:
        model = Accounts
        fields = '__all__'

    def save(self):

        account = super(TransactionForm, self).save(commit = False)

        account.amount = self.cleaned_data.get('amount')
        account.dept_name = self.cleaned_data.get('dept_name')
        account.transaction_type = self.cleaned_data.get('transaction_type')
        account.transactee = self.cleaned_data.get('transactee')
        account.purpose = self.cleaned_data.get('purpose')
        account.date_of_transaction = self.cleaned_data.get('date_of_transaction')
        cur_amt = 0

        try:
            cur_obj = Accounts.objects.filter(dept_name = account.dept_name).last()
            cur_amt = cur_obj.current_balance

        except Exception:
            cur_amt = 0
        
        if account.transaction_type == 'C': account.current_balance = account.amount + cur_amt
        else: account.current_balance = cur_amt - account.amount

        try:
            account.save()
        except Exception:
            Accounts.objects.filter(id = account.id).delete()
            account.save()

        return account
        

