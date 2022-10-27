from rest_framework import generics
from split.serializer import ExpenseSerializer
from split.models import Expense


# NOTE Have a factory here to decide the serializer based on type of split
# Create your views here.
class ExpenseCreate(generics.CreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

class ExpenseRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()

    def perform_destroy(self, instance):
        instance.Group.rebalance(instance.Details, 1)
        return super().perform_destroy(instance)