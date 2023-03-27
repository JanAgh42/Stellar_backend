from rest_framework.decorators import api_view
from ..services import notification_service

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
    return notification_service.new_notification(request)

@api_view(['POST'])
def new_group_notification(request, group_id):
    return notification_service.new_group_notification(request, group_id)