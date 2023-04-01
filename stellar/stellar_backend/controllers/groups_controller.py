from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..services import group_service, session_service
from ..static import constants as const

@api_view(['GET', 'PUT', 'DELETE'])
def manage_single_group(request, group_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return group_service.get_group(group_id)
    elif request.method == 'DELETE':
        return group_service.delete_group(group_id)
    elif request.method == 'PUT':
        return group_service.change_group(request, group_id)
    
@api_view(['GET'])
def get_own_groups(request, user_id):
    return group_service.get_own_groups(user_id)

@api_view(['GET'])
def get_all_groups(request, user_id):
    return group_service.get_all_groups(user_id)

@api_view(['POST'])
def new_group(request):
    return group_service.new_group(request)