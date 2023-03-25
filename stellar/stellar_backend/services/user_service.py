from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.response import Response

from ..serializers import UserSerializer
from ..models import User, GroupsMember

def get_user(user_id):
    try:
        user = User.objects.get(id = user_id)

        user_data = UserSerializer(user).data
        user_data["groups"] = GroupsMember.objects.filter(user_id = user_data["id"]).count()

    except ObjectDoesNotExist:
        return Response("User not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(user_data, status = status.HTTP_200_OK)

def register_user(request):
    try:
        user_serializer = UserSerializer(data = request.data)

        if user_serializer.is_valid():
            user = user_serializer.save()

            return Response("Success", status = status.HTTP_201_CREATED)
    except DatabaseError:
        return Response("User already exists", status = status.HTTP_409_CONFLICT)