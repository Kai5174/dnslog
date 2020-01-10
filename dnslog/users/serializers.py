from rest_framework import serializers
from .models import User, IscanUser

class IscanUserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='userprofile.avatar')
    introduction = serializers.CharField(source='userprofile.introduction')
    roles = serializers.CharField(source='userprofile.role')
    class Meta:
        model = User
        fields = ('username', 'avatar', 'introduction', 'roles')
