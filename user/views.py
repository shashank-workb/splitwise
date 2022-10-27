from rest_framework import generics
from user.serializers import UserSerializer, GroupSerializer
from user.models import User, Group
from rest_framework import serializers
# Create your views here.

class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class UserRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_destroy(self, instance):
        raise serializers.ValidationError('User Deletion Not Allowed')

class GroupCreate(generics.CreateAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

class GroupRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = GroupSerializer
    queryset = Group.objects.all()

    def perform_destroy(self, instance):
        GroupSerializer.delete_setup(instance)
        response = super().perform_destroy(instance)
        return response