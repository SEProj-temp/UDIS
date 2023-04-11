from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, ListView
from datetime import date

from .forms import InventoryForm
from .models import Inventory
from accountings.models import Accounts

# Create your views here.

def inventory(request):
    inven = Inventory.objects.all()
    return render(request, 'inventory/invlist.html', {'inventory': inven})

def inv_searcher(request):
    return render(request, 'inventory/invsearch.html')


class InventoryCreate(CreateView):

    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/addinv.html'

    def form_valid(self, form):
        
        dept_bal = Accounts.objects.filter(dept_name = form.cleaned_data['dept_name']).last().current_balance
        funds_reqd = form.cleaned_data['price'] * form.cleaned_data['quantity']
        
        if dept_bal < funds_reqd:

            messages.error(self.request, "Ouch! There aren't enough funds to allocate to the project!")
            return redirect(self.request.path)
        
        user = self.request.user
        inven = form.save()

        Accounts.objects.create(
            dept_name = inven.dept_name,
            amount = funds_reqd,
            transaction_type = 'D',
            transactee = f"Secretary {user.username}",
            purpose = f"Furniture {inven.furniture_name} allocation",
            date_of_transaction = date.today(),
            current_balance = dept_bal - funds_reqd
            )

        if inven:
            messages.success(self.request, f'Furniture {inven.furniture_name} added successfully!')
            return redirect('allinv')
        
class InventoryUpdate(UpdateView):

    model = Inventory
    form_class = InventoryForm
    template_name = 'inventory/addinv.html'

    def form_valid(self, form):

        dept_bal = Accounts.objects.filter(dept_name = form.cleaned_data['dept_name']).last().current_balance
        
        user = self.request.user
        pk = self.kwargs['pk']
        inven = Inventory.objects.filter(id = pk).first()

        if inven.dept_name != user.dept_name:
            messages.error(self.request, 'Can not edit the inventories of another department!')
            return inventory(self.request)
        
        if 'price' in form.changed_data or 'quantity' in form.changed_data:

            acc = Accounts.objects.filter(purpose = f"Furniture {inven.furniture_name} allocation").last()
            funds_reqd = form.cleaned_data['price'] * form.cleaned_data['quantity']
            extra_funds = funds_reqd - acc.amount

            if dept_bal < extra_funds:

                messages.error(self.request, "Ouch! There aren't enough funds to allocate to the project!")
                return redirect(self.request.path)
            
            Accounts.objects.create(
                dept_name = inven.dept_name,
                amount = funds_reqd,
                transaction_type = 'D',
                transactee = f"Secretary {user.username}",
                purpose = f"Furniture {inven.furniture_name} allocation",
                date_of_transaction = date.today(),
                current_balance = dept_bal - extra_funds
                )
        
        inven = form.save()

        if inven:
            messages.success(self.request, f'Furniture {inven.furniture_name} updated successfully!')
            return redirect('allinv')
        
class InventorySearch(ListView):

    model = Inventory
    template_name = 'inventory/invlist.html'
    context_object_name = 'inventory'

    def get_queryset(self):
        
        fur_name = self.request.GET.get('fur_name')
        fur_type = self.request.GET.get('fur_type')
        
        if fur_name == '':
            if fur_type == '':
                inventory = Inventory.objects.all()
            
            else:
                inventory = Inventory.objects.filter(furniture_type = fur_type)
        else:
            if fur_type == '':
                inventory = Inventory.objects.filter(furniture_name__contains = fur_name)
            
            else:
                inventory = Inventory.objects.filter(furniture_name__contains = fur_name, furniture_type = fur_type)
        return inventory