from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..services import notification_service, session_service
from ..static import constants as const

@api_view(['GET'])
def get_notifications(request, user_id):
    return notification_service.get_notifications(user_id)

@api_view(['DELETE'])
def delete_notification(request, notif_id):
    return notification_service.delete_notification(notif_id)

@api_view(['DELETE'])
def delete_user_notifications(request, user_id):
    return notification_service.delete_user_notifications(user_id)

@api_view(['POST'])
def new_notification(request):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return notification_service.new_notification(request.data)

@api_view(['POST'])
def new_group_notification(request, group_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)
    
    return notification_service.new_group_notification(request, group_id)