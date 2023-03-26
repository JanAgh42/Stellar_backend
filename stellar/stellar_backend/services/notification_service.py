from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import NotificationSerializer
from ..models import Notification

def get_notifications(user_id):
    notifications = Notification.objects.filter(user_id = user_id)

    notifs_data = NotificationSerializer(notifications, many = True).data

    return Response(notifs_data, status = status.HTTP_200_OK)

def delete_notification(notif_id):
    try:
        notification = Notification.objects.get(id = notif_id)

        notification.delete()
    except ObjectDoesNotExist:
        return Response("Notification not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)

def delete_user_notifications(user_id):
    try:
        notifications = Notification.objects.filter(user_id = user_id)

        notifications.delete()
    except ObjectDoesNotExist:
        return Response("One or more notifications not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)