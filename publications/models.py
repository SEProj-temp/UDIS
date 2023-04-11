from django.db import models

# Create your models here.

class Publications(models.Model):
    '''
    A class of models that creates the database of publications, classified by department names.
    '''

    dept_name = models.CharField(max_length = 100) #For the storage of different department names.
    pub_title = models.CharField(max_length = 100, unique = True) #For the storage of publication titles.
    pub_author = models.CharField(max_length = 500) #For the storage of author names.
    pub_date = models.DateField()
