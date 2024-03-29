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

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Notification
        fields = ['id', 'user_id', 'message', 'date']

class GroupsMemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = GroupsMember
        fields = ['id', 'user_id', 'group_id', 'is_owner']

class MessageSerializer(serializers.ModelSerializer):
    reply_to_id = serializers.CharField(allow_blank = True)
    class Meta:
        model = Message
        fields = ['id', 'user_id', 'group_id', 'reply_to_id', 'message', 'date', 'location', 'image_url']