from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'image_url', 'personal_color']

class SignInSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignInData
        fields = ['user_id', 'email', 'password']

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionToken
        fields = ['user_id', 'token', 'date']

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ['id', 'name', 'owner_id', 'category', 'icon', 'banner_color', 'icon_background_color']

class GroupsMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupsMember
        fields = ['user_id', 'group_id', 'is_owner']