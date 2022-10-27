from django.db import models
from user.models import Group

# Create your models here.
# NOTE improvements on how to refer releted models
# Include field to identify what kind of split is there
class Expense(models.Model):
    Title = models.CharField(max_length=100)
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    Amount = models.IntegerField()
    Details = models.JSONField()

    def __str__(self):
        return self.Title

'''
class Transaction(models.Model):
    Source = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    Destination = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='+')
    Expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    Amount = models.IntegerField()
'''

    
