from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from rest_framework import status
from rest_framework.response import Response

from ..serializers import UserSerializer
from ..models import User, GroupsMember, SignInData, Message
from ..static import constants as const

from .sign_in_data_service import create_register_entry as register, validate_auth
from .session_service import create_user_token, get_user_token
from .usergroup_service import num_where_is_owner

def get_user(user_id):
    try:
        user = User.objects.get(id = user_id)

        user_data = UserSerializer(user).data
        user_data["groups"] = GroupsMember.objects.filter(user_id = user_data["id"]).count()
        user_data["posts"] = Message.objects.filter(user_id = user_id).count()
        user_data["own_groups"] = num_where_is_owner(user_id)
        user_data["email"] = SignInData.objects.get(user_id = user_data["id"]).email

    except ObjectDoesNotExist:
        return Response(const.USER_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
    return Response(user_data, status = status.HTTP_200_OK)

def register_user(request):
    try:
        user_serializer = UserSerializer(data = request.data)

        if user_serializer.is_valid():
            user = user_serializer.save()

            register(request, str(user.id))
            
            token = create_user_token(str(user.id))

            return Response({
                "user_id": str(user.id),
                "token": token
            }, status = status.HTTP_201_CREATED)
    except DatabaseError:
        delete_user(str(user.id))
        return Response(const.USER_EXISTS, status = status.HTTP_409_CONFLICT)
    
def authenticate_user(request):
    try:
        auth = validate_auth(request.data)

        if auth != None:
            token = get_user_token(auth["user_id"])

            return Response({
                    "user_id": str(auth["user_id"]),
                    "token": token
                }, status = status.HTTP_200_OK)
    except ObjectDoesNotExist:
        pass
    return Response(const.LOGIN_FAILED, status.HTTP_401_UNAUTHORIZED)
    
def change_user(request, user_id):
    try:
        old_user = User.objects.get(id = user_id)
        updated_user = UserSerializer(old_user, data = request.data)

        if updated_user.is_valid():
            updated_user.save()

            return Response(status = status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(const.USER_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
def delete_user(user_id):
    user = User.objects.get(id = user_id)
    user.delete()