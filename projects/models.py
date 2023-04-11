from django.db import models
# Create your models here.

class Projects(models.Model):
    '''
    A class of models that creates the database of projects, classified by department names.
    '''

    project_name = models.CharField(max_length = 200, unique = True) #Name of the project
    dept_name = models.CharField(max_length = 100) #For the storage of different department names.
    faculty_name = models.CharField(max_length = 100) #The head of the project, whom a student has to contact.
    
    STATUS_CHOICES = (
        ('', "Select status"),
        ('O', "Ongoing"),
        ('C', "Completed"),
    )

    status = models.CharField(max_length = 1, choices = STATUS_CHOICES, default = '')
    
    MONTH_CHOICES = tuple((m, m) for m in range(13))
    
    duration_year = models.IntegerField()
    duration_month = models.IntegerField(choices = MONTH_CHOICES, default = 0)
    allocated_funds = models.PositiveIntegerField()
