from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from rest_framework import status
from rest_framework.response import Response

from ..serializers import UserSerializer
from ..models import User, GroupsMember

from .sign_in_data_service import create_register_entry as register, validate_auth
from .session_service import create_user_token, get_user_token

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

            if not register(request, str(user.id)):
                raise DatabaseError()
            
            token = create_user_token(str(user.id))

            return Response({
                "user_id": str(user.id),
                "token": token
            }, status = status.HTTP_201_CREATED)
    except DatabaseError:
        return Response("User already exists", status = status.HTTP_409_CONFLICT)
    
def authenticate_user(request):
    try:
        auth = validate_auth(request.data)
        token = get_user_token(auth["user_id"])

        return Response({
                "user_id": str(auth["user_id"]),
                "token": token
            }, status = status.HTTP_200_OK)

    except ObjectDoesNotExist:
        return Response("Invalid credentials", status.HTTP_401_UNAUTHORIZED)