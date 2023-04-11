from django import forms
from .models import Projects

class ProjectForm(forms.ModelForm):
    '''
    A form to enter the details of a new department project/research 
    '''

    project_name = forms.CharField(max_length = 200, required = True, widget=forms.TextInput(attrs={'placeholder': 'Project Name'})) #Name of the project
    dept_name = forms.CharField(max_length = 100, required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'})) #For the storage of different department names.
    faculty_name = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Faculty Name'})) #The head of the project, whom a student has to contact.
    status = forms.ChoiceField(choices = Projects.STATUS_CHOICES, required = True)
    
    duration_year = forms.IntegerField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Enter yearly duration'}))
    duration_month = forms.ChoiceField(choices = Projects.MONTH_CHOICES, required = True)
    allocated_funds = forms.IntegerField(min_value = 0, required = True)

    class Meta:

        model = Projects
        fields = '__all__'

    def save(self):

        project = super(ProjectForm, self).save(commit = False)

        project.project_name = self.cleaned_data.get('project_name')
        project.dept_name = self.cleaned_data.get('dept_name')
        project.faculty_name = self.cleaned_data.get('faculty_name')
        project.status = self.cleaned_data.get('status')
        project.duration_year = self.cleaned_data.get('duration_year')
        project.duration_month = self.cleaned_data.get('duration_month')
        project.allocated_funds = self.cleaned_data.get('allocated_funds')

        try:
            project.save()

        except Exception:

            Projects.objects.filter(id = project.id).delete()
            project.save()

        return project
