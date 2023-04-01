from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..services import message_service, session_service
from ..static import constants as const

@api_view(['POST'])
def new_message(request):
    return message_service.new_message(request)

@api_view(['GET'])
def get_message_content(request, message_id):
    return message_service.get_message_content(message_id)

@api_view(['GET'])
def get_group_messages(request, group_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return message_service.get_group_messages(group_id)

@api_view(['DELETE'])
def delete_message(request, message_id):
    return message_service.delete_message(message_id)

@api_view(['DELETE'])
def delete_group_messages(request, group_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return message_service.delete_group_messages(group_id)

@api_view(['PUT'])
def change_message(request, message_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return message_service.change_message(request, message_id)