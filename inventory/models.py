from django.db import models

# Create your models here.

class Inventory(models.Model):
    """
    A class of models that stores the furniture iventory of the department.
    """

    dept_name = models.CharField(max_length = 200)
    furniture_name = models.CharField(max_length = 200, unique = True)
    furniture_type = models.CharField(max_length = 200)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    location = models.CharField(max_length = 200)