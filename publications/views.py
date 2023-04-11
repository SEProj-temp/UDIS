from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView

from .forms import PublicationForm
from .models import Publications

# Create your views here.

def allpubs(request):

    publis = Publications.objects.all()
    return render(request, 'publications/publist.html', {'publis': publis})

class PublicationCreate(CreateView):

    model = Publications
    form_class = PublicationForm
    template_name = 'publications/addpubs.html'

    def form_valid(self, form):

        publi = form.save()

        if publi:
            messages.success(self.request, f'Publication {publi.pub_title} added successfully!')
            return redirect('allpubs')
        
class PublicationUpdate(UpdateView):

    model = Publications
    form_class = PublicationForm
    template_name = 'publications/addpubs.html'

    def form_valid(self, form):

        publi = form.save()

        if publi:
            messages.success(self.request, f'Publication {publi.pub_title} updated successfully!')
            return redirect('allpubs')