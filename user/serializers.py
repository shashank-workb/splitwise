from rest_framework import serializers
from user.models import User, Group

class UserSerializer(serializers.ModelSerializer):
    Groups = serializers.ListField(child=serializers.CharField(), default=[], required=False)

    class Meta:
        model = User
        fields = ('Name', 'Groups', 'Balance')
        extra_kwargs = {
            'Groups':{'read_only': True},
            'Balance': {'read_only': True}}

class GroupSerializer(serializers.ModelSerializer):
    Users = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    
    @staticmethod
    def can_be_deleted(instance, usernames):
        for user1 in usernames:
            for user2 in instance.Users:
                if user1 == user2:
                    continue
                sorted_users = sorted([user1, user2])
                key = sorted_users[0] + '__' + sorted_users[1]
                if instance.PayMap[key] != 0:
                    return False
        
        return True

    def add_groups_to_users(self, usernames, group_name):
        for username in usernames:
            obj = User.objects.get_or_create(Name=username)[0]
            if group_name not in obj.Groups: 
                obj.Groups.append(group_name)
                obj.save()
    
    def remove_groups_from_users(self, remove_group_from_users, group):
        for user in remove_group_from_users:
            obj = User.objects.get(Name=user)
            obj.Groups.remove(group)
            obj.save()

    @staticmethod
    def delete_setup(instance):
        if not GroupSerializer.can_be_deleted(instance, instance.Users):
            raise serializers.ValidationError(f'Group cant be deleted as payment not settled')

        usernames = instance.Users
        if usernames:
            obj = GroupSerializer()
            obj.remove_groups_from_users(usernames, instance.Title)


    def update(self, instance, validated_data):
        if validated_data.get('Title'):
            raise serializers.ValidationError('Cant update title of Group')
        usernames = validated_data.get('Users')
        if usernames:
            remove_group_from_users = [user for user in instance.Users if user not in usernames]
            if not GroupSerializer.can_be_deleted(instance, remove_group_from_users):
                raise serializers.ValidationError(f'Users {str(remove_group_from_users)} cant be deleted as payment not settled')
            self.remove_groups_from_users(remove_group_from_users, validated_data['Title'])
            self.add_groups_to_users(usernames, validated_data['Title'])
        
        return super().update(instance, validated_data)


    def create(self, validated_data):
        self.add_groups_to_users(validated_data['Users'], validated_data['Title'])
        validated_data['PayMap'] = {}
        sorted_users = validated_data['Users'] = sorted(validated_data['Users'])
        for i in range(len(sorted_users)):
            for j in range(i+1, len(sorted_users)):
                key = sorted_users[i] + '__' + sorted_users[j]
                validated_data['PayMap'][key] = 0
        instance = super().create(validated_data)
        return instance

    class Meta:
        model = Group
        fields = '__all__'
        extra_kwargs = {'SimplifyDebt': {'required': False}}

