from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView
from datetime import date

from .forms import ProjectForm
from .models import Projects
from accountings.models import Accounts

# Create your views here.

def allprojects(request):
    projects = Projects.objects.all()
    return render(request, 'projects/plist.html', {'projects': projects})

class ProjectCreateForm(CreateView):

    model = Projects
    form_class = ProjectForm
    template_name = 'projects/addproj.html'

    def form_valid(self, form):

        dept_bal = Accounts.objects.filter(dept_name = form.cleaned_data['dept_name']).last().current_balance

        if dept_bal < form.cleaned_data['allocated_funds']:

            messages.error(self.request, "Ouch! There aren't enough funds to allocate to the project!")
            return redirect(self.request.path)
        
        user = self.request.user
        project = form.save()

        Accounts.objects.create(
            dept_name = project.dept_name,
            amount = project.allocated_funds,
            transaction_type = 'D',
            transactee = f"Secretary {user.username}",
            purpose = f"Project {project.project_name} allocation",
            date_of_transaction = date.today(),
            current_balance = dept_bal - project.allocated_funds
            )
        
        if project:
            messages.success(self.request, f'Project {project.project_name} added successfully!')
            return redirect('allprojects')
        
class ProjectUpdate(UpdateView):

    model = Projects
    form_class = ProjectForm
    template_name = 'projects/addproj.html'

    def form_valid(self, form):

        if 'status' in form.changed_data and form.cleaned_data['status'] == 'O':
            form.cleaned_data['status'] = 'C'

        dept_bal = Accounts.objects.filter(dept_name = form.cleaned_data['dept_name']).last().current_balance

        user = self.request.user
        pk = self.kwargs['pk']
        proj = Projects.objects.filter(id = pk).first()
        
        if proj.dept_name != user.dept_name:
            messages.error(self.request, 'Can not edit the projects of another department!')
            return allprojects(self.request)

        if 'allocated_funds' in form.changed_data:

            acc = Accounts.objects.filter(purpose = f"Project {proj.project_name} allocation").last()
            extra_funds = form.cleaned_data['allocated_funds'] - acc.amount

            if dept_bal < extra_funds:

                messages.error(self.request, "Ouch! There aren't enough funds to allocate to the project!")
                return redirect(self.request.path)
            
            Accounts.objects.create(
                dept_name = proj.dept_name,
                amount = form.cleaned_data['allocated_funds'],
                transaction_type = 'D',
                transactee = f"Secretary {user.username}",
                purpose = f"Project {proj.project_name} allocation",
                date_of_transaction = date.today(),
                current_balance = dept_bal - extra_funds
                )
        
        project = form.save()
        
        if project:
            messages.success(self.request, f'Project {project.project_name} updated successfully!')
            return redirect('allprojects')