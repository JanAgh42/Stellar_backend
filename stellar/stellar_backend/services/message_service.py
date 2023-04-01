from django.db import DatabaseError
from django.http import QueryDict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import MessageSerializer
from ..models import Message, User
from ..static import constants as const

from .notification_service import new_notification

def new_message(request):
    try:
        if isinstance(request.data, QueryDict):
            request.data._mutable = True

        if request.data["reply_to_id"] is None:
            request.data["reply_to_id"] = ""

        message_serializer = MessageSerializer(data = request.data)

        if message_serializer.is_valid():        
            message = message_serializer.save()

            if message.reply_to_id != "":
                new_notification({
                    "user_id": message.reply_to_id,
                    "message":"user replied to your message"
                })

            return Response({"message_id": str(message.id)}, status = status.HTTP_201_CREATED)
        
    except DatabaseError:
        return Response(const.M_CANNOT_CREATE, status = status.HTTP_400_BAD_REQUEST)

def get_message_content(message_id):
    try:
        message = Message.objects.get(id = message_id)
        message_data = MessageSerializer(message).data

        user_name = User.objects.get(id = message_data["user_id"]).name

        if message_data["reply_to_id"] != "":
            reply_to = User.objects.get(id = message_data["reply_to_id"]).name
            message_data["reply_to_id"] = reply_to
        else:
            message_data["reply_to_id"] = None
        
        message_data["user_id"] = user_name
    except ObjectDoesNotExist:
        return Response(const.MESSAGE_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
    return Response(message_data, status = status.HTTP_200_OK)

def delete_message(message_id):
    try:
        message = Message.objects.get(id = message_id)
        message.delete()
    except ObjectDoesNotExist:
        return Response(const.MESSAGE_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)

def delete_group_messages(group_id):
    try:
        messages = Message.objects.filter(group_id = group_id)

        messages.delete()
    except ObjectDoesNotExist:
        return Response(const.MESSAGES_MISSING, status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)    

def change_message(request, message_id):
    try:
        old_message = Message.objects.get(id = message_id)
        updated_message = MessageSerializer(old_message, data = request.data)

        if updated_message.is_valid():
            updated_message.save()

            return Response(status = status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(const.MESSAGE_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
def get_group_messages(group_id):
    messages = Message.objects.filter(group_id = group_id)

    messages_data = MessageSerializer(messages, many = True).data
    
    return Response(messages_data, status = status.HTTP_200_OK)