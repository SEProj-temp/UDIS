from django.db import models

# Create your models here.
class Accounts(models.Model):
    '''
    Class storing details of all credits and debits, in reverse chronological order.
    '''

    dept_name = models.CharField(max_length = 200)
    amount = models.PositiveIntegerField()

    TYPE_CHOICES = (
        ('C', "Credit"),
        ('D', "Debit")
    )

    transaction_type = models.CharField(max_length = 1, choices = TYPE_CHOICES, default = 'C')
    transactee = models.CharField(max_length = 200)
    purpose = models.TextField(max_length = 500)
    date_of_transaction = models.DateField()
    current_balance = models.PositiveIntegerField(default = 0)


