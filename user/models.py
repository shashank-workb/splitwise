from django.db import models
from django.contrib.postgres.fields import ArrayField

class User(models.Model):
    Name = models.CharField(max_length=100, primary_key=True)
    Groups = ArrayField(models.CharField(max_length=100), default=list, blank=True)
    Balance = models.JSONField(null=True, default=dict)

    def rebalance(self, expense):
        Payer = self.Name
        for borrower in expense:
            if borrower not in [Payer,'Payer']:
                key = '__'.join(sorted([Payer, borrower]))
                if key not in self.Balance:
                    self.Balance[key] = 0
                if Payer < borrower:
                    self.Balance[key] += expense[borrower]
                else:
                    self.Balance[key] -= expense[borrower]
                self.rebalance_counter(borrower, key, self.Balance[key])
        self.save()

    def rebalance_counter(self, username, key, value):
        counter_user = User.objects.filter(Name=username).first()
        if key not in counter_user.Balance:
            counter_user.Balance[key] = 0
        counter_user.Balance[key] = value

        counter_user.save()

    def __str__(self):
        return self.Name

# NOTE: Created at, Updated at, Use manytomany
class Group(models.Model):
    Title = models.CharField(max_length=100, primary_key=True)
    Users = ArrayField(models.CharField(max_length=100))
    SimplifyDebt = models.BooleanField(default=False)
    PayMap = models.JSONField(null=True)

    def rebalance(self, expense, reverse=0):
        if reverse:
            for each in expense:
                if each != 'Payer' and each != expense['Payer']:
                    expense[each] = -1 * expense[each]
        Payer = expense['Payer']
        for borrower in expense:
            if borrower not in [Payer,'Payer']:
                key = '__'.join(sorted([Payer, borrower]))
                if Payer < borrower:
                    self.PayMap[key] += expense[borrower]
                else:
                    self.PayMap[key] -= expense[borrower]
        self.save()
        User.objects.filter(Name=expense['Payer']).first().rebalance(expense)
                

    def __str__(self):
        return self.Title

