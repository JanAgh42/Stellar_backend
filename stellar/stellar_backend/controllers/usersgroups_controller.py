from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..services import usergroup_service, session_service
from ..static import constants as const

@api_view(['POST'])
def add_user_to_group(request):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return usergroup_service.add_user_to_group(request.data)

@api_view(['GET'])
def is_member_of_group(request, user_id, group_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return usergroup_service.is_member_of_group(user_id, group_id)

@api_view(['DELETE'])
def delete_user_from_group(request, user_id, group_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return usergroup_service.delete_user_from_group(user_id, group_id)

@api_view(['GET'])
def num_where_is_owner(request, user_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return usergroup_service.num_where_is_owner(user_id)