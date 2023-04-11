from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    '''
    The extension of the abstractuser class, that defines boolean fields to
    distinguish between user classes. Stored as an SQL table in Postgres
    '''

    email = models.EmailField(unique = True)
    is_student = models.BooleanField(default = False)
    is_faculty = models.BooleanField(default = False)
    is_secretary = models.BooleanField(default = False)

    first_name = models.CharField(max_length = 80)
    last_name = models.CharField(max_length = 80)
    dept_name = models.CharField(max_length = 80)
    address = models.CharField(max_length = 200)

    GENDER_CHOICES = (
        ('', 'Select a gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )
    
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = '')
    phone_number = models.CharField(max_length = 10)
    year_of_admission = models.PositiveIntegerField(null = True, blank = True)
    
class Student(User):
    '''
    Class Student, that extends on the defined abstract User class
    '''

    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, related_name = 'stu')

    PROGRAMME_CHOICES = (
        ('', 'Select a Programme'),
        ('BT', "Bachelor of Technology"),
        ('MT', "Master of Technology"),
        ('PhD', "Doctor of Philosophy"),
        ('MSc', "Master of Science"),
        ('BSc', "Bachelor of Science"),
        ('DD', "Dual Degree"),
    )
    programme = models.CharField(max_length = 3, choices = PROGRAMME_CHOICES, default = '')
    guardian_name = models.CharField(max_length = 80)
    


    
    
