from django.db import DatabaseError
from django.http import QueryDict
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import MessageSerializer, UserSerializer
from ..models import Message, User

def new_message(request):
    try:
        if isinstance(request.data, QueryDict):
            request.data._mutable = True

        if request.data["reply_to_id"] is None:
            request.data["reply_to_id"] = ""

        message_serializer = MessageSerializer(data = request.data)

        if message_serializer.is_valid():        
            message = message_serializer.save()
        
            return Response({"message_id": str(message.id)}, status = status.HTTP_201_CREATED)
        else: return Response("serializer not valid", status = status.HTTP_300_MULTIPLE_CHOICES)
    except DatabaseError:
        return Response("Can't create message", status = status.HTTP_400_BAD_REQUEST)

def get_message_content(message_id):
    try:
        message = Message.objects.get(id = message_id)
        message_data = MessageSerializer(message).data

        user = User.objects.get(id = message_data["user_id"])

        if message_data["reply_to_id"] is not "":
            reply_to = User.objects.get(id = message_data["reply_to_id"])
            message_data["reply_to_id"] = reply_to.name
        else:
            message_data["reply_to_id"] = None
        
        message_data["user_id"] = user.name
    except ObjectDoesNotExist:
        return Response("Message not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(message_data, status = status.HTTP_200_OK)

def delete_message(message_id):
    try:
        message = Message.objects.get(id = message_id)
        message.delete()
    except ObjectDoesNotExist:
        return Response("Can't delete message", status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)

def delete_group_messages(group_id):
    try:
        messages = Message.objects.filter(group_id = group_id)

        messages.delete()
    except ObjectDoesNotExist:
        return Response("One or more messages not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)    

def change_message(request, message_id):
    try:
        old_message = Message.objects.get(id = message_id)
        updated_message = MessageSerializer(old_message, data = request.data)

        if updated_message.is_valid():
            updated_message.save()

            return Response(status = status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response("Message not found", status = status.HTTP_404_NOT_FOUND)
    
def get_group_messages(group_id):
    messages = Message.objects.filter(group_id = group_id)

    messages_data = MessageSerializer(messages, many = True).data
    
    return Response(messages_data, status = status.HTTP_200_OK)