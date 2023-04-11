from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Student
from django.db import connection
from datetime import date


class StudentSignUpForm(UserCreationForm):
    '''
    A form for Student User Creation, extending the abstract UserCreationForm class
    '''

    first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    dept_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'}))
    address = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Address'}))

    gender = forms.ChoiceField(choices = User.GENDER_CHOICES)

    email = forms.EmailField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Email ID'}))
    programme = forms.ChoiceField(choices = Student.PROGRAMME_CHOICES)
    
    guardian_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': "Guardian's Name"}))
    phone_number = forms.CharField(min_length = 10, max_length = 10, required = True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    year_of_admission = forms.IntegerField(max_value = date.today().year, min_value = 0, required = True, widget = forms.TextInput(attrs={'placeholder': 'Admission Year'}))
    
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):

        user = super(StudentSignUpForm, self).save(commit = False)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.dept_name = self.cleaned_data.get('dept_name')
        user.address = self.cleaned_data.get('address')
        user.gender = self.cleaned_data.get('gender')
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.year_of_admission = self.cleaned_data['year_of_admission']
        
        user.is_student = True
        
        try:
            user.save()
        except Exception:
            User.objects.filter(id = user.id).delete()
            user.save()

        idd = User.objects.last().id
        
        student = Student.objects.create(user = user)
        student.programme = self.cleaned_data.get('programme')
        student.guardian_name = self.cleaned_data.get('guardian_name')

        student.save()

        with connection.cursor() as cursor:
            
            #Change the row created in the student database, as there would be a mismatch of the user pointer and the user object 
            cursor.execute("UPDATE accounts_student SET user_ptr_id = %s WHERE user_id = %s", [idd, idd])
            #Delete the empty row thusly created in the User table.
            cursor.execute("DELETE FROM accounts_user WHERE id = %s", [idd + 1])

        return user

class FacultySignUpForm(UserCreationForm):
    '''
    A form for Faculty User Creation, extending the abstract UserCreationForm class
    '''
    
    first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    dept_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'}))
    address = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Address'}))

    gender = forms.ChoiceField(choices = User.GENDER_CHOICES)

    email_id = forms.EmailField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Email ID'}))
    phone_number = forms.CharField(min_length = 10, max_length = 10, required = True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    year_of_admission = forms.IntegerField(max_value = date.today().year, min_value = 0, required = True, widget = forms.TextInput(attrs={'placeholder': 'Admission Year'}))

    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):

        user = super(FacultySignUpForm, self).save(commit = False)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.dept_name = self.cleaned_data.get('dept_name')
        user.address = self.cleaned_data.get('address')
        user.gender = self.cleaned_data.get('gender')
        user.year_of_admission = self.cleaned_data['year_of_admission']
        
        user.is_faculty = True
        user.email = self.cleaned_data.get('email_id')
        user.phone_number = self.cleaned_data.get('phone_number')

        try:
            user.save()
        except Exception:
            User.objects.filter(id = user.id).delete()
            user.save()
            
        return user
    
class SecretarySignUpForm(UserCreationForm):
    '''
    A form for Secretary User Creation, extending the abstract UserCreationForm class
    '''
    
    first_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    dept_name = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Department Name'}))
    address = forms.CharField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Address'}))

    gender = forms.ChoiceField(choices = User.GENDER_CHOICES)

    email_id = forms.EmailField(required = True, widget=forms.TextInput(attrs={'placeholder': 'Email ID'}))
    phone_number = forms.CharField(min_length = 10, max_length = 10, required = True, widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}))
    year_of_admission = forms.IntegerField(max_value = date.today().year, min_value = 0, required = True, widget = forms.TextInput(attrs={'placeholder': 'Admission Year'}))
    
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self):

        user = super(SecretarySignUpForm, self).save(commit = False)

        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.dept_name = self.cleaned_data.get('dept_name')
        user.address = self.cleaned_data.get('address')
        user.gender = self.cleaned_data.get('gender')
        user.year_of_admission = self.cleaned_data['year_of_admission']
        
        user.is_secretary = True
        user.email = self.cleaned_data.get('email_id')
        user.phone_number = self.cleaned_data.get('phone_number')

        try:
            user.save()
        except Exception:
            User.objects.filter(id = user.id).delete()
            user.save()

        return user
