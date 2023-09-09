from rest_framework import serializers
from django.contrib.auth.models import User

from .models import PeriodCycle, PersonalInfo, ChatInfo

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        return user


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodCycle
        fields = ['start_date', 'cycle_length']

class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalInfo
        fields = ['age', 'weight', 'height', 'cramps', 'feeling_tired']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatInfo
        fields = ['content']

class MessageSerializer(serializers.Serializer):
    role = serializers.CharField(max_length=10)
    content = serializers.CharField()

# {
#     "username": "Kamila", 
#     "email": "tashimovakamila1@gmail.com", 
#     "first_name": "Kamila", 
#     "last_name": "Tashimova", 
#     "password": "Bota456"
# }