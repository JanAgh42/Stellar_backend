from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import MessageSerializer, UserSerializer
from ..models import Message, User

def new_message(request):
    try:
        message_serializer = MessageSerializer(data = request.data)
        if message_serializer.is_valid():
            message = message_serializer.save()
        
        return Response({"message_id": str(message.id)}, status = status.HTTP_201_CREATED)
    
    except:
        return Response("Can't create message", status = status.HTTP_400_BAD_REQUEST)

def message_content(request, message_id):
    try:
        message = Message.objects.get(id = message_id)
        message_data = MessageSerializer(message).data

        user = User.objects.get(id = message_data["user_id"])
        user_data = UserSerializer(user).data
        #osetrit null
        reply_to = User.objects.get(id = message_data["reply_to_id"])
        reply_to_data = UserSerializer(reply_to).data

        message_data["user_id"] = user_data["name"]
        message_data["reply_to_id"] = reply_to_data["name"]

    except ObjectDoesNotExist:
        return Response("Message not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(message_data, status = status.HTTP_200_OK)

def delete_message(request, message_id):
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