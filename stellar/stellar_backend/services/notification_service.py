from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from rest_framework import status
from rest_framework.response import Response

from ..serializers import NotificationSerializer
from ..models import GroupsMember, Notification

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

def new_notification(request):
    try:
        notification_serializer = NotificationSerializer(data = request.data)

        if notification_serializer.is_valid():
            notification = notification_serializer.save()

            return Response({"notification_id": str(notification.id)}, status = status.HTTP_201_CREATED)

    except DatabaseError:
        return Response("Can't create notification", status = status.HTTP_400_BAD_REQUEST)
    
def new_group_notification(request, group_id):

    try:
        group_users = GroupsMember.objects.filter(group_id = group_id)
        counter = 0

        for user in group_users:
            notification_serializer = NotificationSerializer(data = request.data)
            notification_serializer.user_id = user.id

            if notification_serializer.is_valid():
                notification_serializer.save()
                counter += 1
        if group_users.__len__() == counter:
            return Response("Notifications created", status = status.HTTP_201_CREATED)
        else:
            return Response("Can't create notifications", status = status.HTTP_400_BAD_REQUEST)
        
    except DatabaseError:
        return Response("Can't create notifications", status = status.HTTP_400_BAD_REQUEST)
