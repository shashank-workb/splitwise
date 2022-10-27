from queue import Empty
from rest_framework import serializers
from user.models import User, Group
from split.models import Expense
from user.serializers import GroupSerializer


class ExpenseSerializer(serializers.ModelSerializer):
    def user_validation(self, values):
        for user in values["Details"]:
            if user == "Payer":
                user = values['Details']['Payer']
            obj = User.objects.filter(Name=user)
            if not obj:
                raise serializers.ValidationError({user: f"User {user} Does not exist"})

        Group_members = values["Group"].Users
        for user in values["Details"]:
            if user != 'Payer' and user not in Group_members:
                raise serializers.ValidationError(
                    {user: f"User {user} not part of the group"}
                )

    def Details_validation(self, values):
        total = 0
        for user in values['Details']:
            if user != 'Payer':
                total += values['Details'][user]
        if total != values['Amount']:
            raise serializers.ValidationError(
                {'details': "Total does not sum up"}
            )
    
    def create(self, validated_data):
        validated_data['Group'].rebalance(dict(validated_data['Details']))
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        expense = dict(instance.Details)
        obj = super().update(instance, validated_data)
        obj.Group.rebalance(expense, 1)
        obj.Group.rebalance(dict(validated_data['Details']))
        return obj

    def validate(self, values):
        self.user_validation(values)
        self.Details_validation(values)
        return values

    class Meta:
        model = Expense
        fields = ("id", "Title", "Group", "Details", "Amount")
