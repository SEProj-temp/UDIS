from django import forms
from .models import Publications

class PublicationForm(forms.ModelForm):
    '''
    A form to enter the details of a new department publication
    '''

    dept_name = forms.CharField(max_length = 100, required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'})) #To store the department names
    pub_title = forms.CharField(max_length = 100, required = True, widget=forms.TextInput(attrs={'placeholder': 'Publication Title'})) # To store the publication titles.
    pub_author = forms.CharField(max_length = 500, required = True, widget=forms.TextInput(attrs={'placeholder': 'Authors (may be comma separated too)'})) #The authors of the publication
    pub_date = forms.DateField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Date of publication'}))

    class Meta:

        model = Publications
        fields = '__all__'

    def save(self):

        publi = super(PublicationForm, self).save(commit = False)

        publi.dept_name = self.cleaned_data.get('dept_name')
        publi.pub_title = self.cleaned_data.get('pub_title')
        publi.pub_author = self.cleaned_data.get('pub_author')
        publi.pub_date = self.cleaned_data.get('pub_date')

        try:
            publi.save()

        except Exception:

            Publications.objects.filter(id = publi.id).delete()
            publi.save()

        return publi