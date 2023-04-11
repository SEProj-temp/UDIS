from django import forms
from .models import Inventory

class InventoryForm(forms.ModelForm):
    '''
    A form to enter the details of a new furniture type
    '''

    furniture_name = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Furniture Name'})) #Name of the inven
    dept_name = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'})) #For the storage of different department names.
    furniture_type = forms.CharField(max_length = 200, widget=forms.TextInput(attrs={'placeholder': 'Furniture Type'})) #The head of the inven, whom a student has to contact.
    price = forms.IntegerField(min_value = 0, required = True, widget=forms.TextInput(attrs={'placeholder': 'Price (in Rs)'}))
    quantity = forms.IntegerField(min_value = 0, required = True, widget=forms.TextInput(attrs={'placeholder': 'Quantity'}))
    location = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Location'})) #Name of the location

    class Meta:

        model = Inventory
        fields = '__all__'

    def save(self):

        inven = super(InventoryForm, self).save(commit = False)

        inven.furniture_name = self.cleaned_data.get('furniture_name')
        inven.dept_name = self.cleaned_data.get('dept_name')
        inven.furniture_type = self.cleaned_data.get('furniture_type')
        inven.price = self.cleaned_data.get('price')
        inven.quantity = self.cleaned_data.get('quantity')
        inven.location = self.cleaned_data.get('location')

        try:
            inven.save()

        except Exception:

            Inventory.objects.filter(id = inven.id).delete()
            inven.save()

        return inven