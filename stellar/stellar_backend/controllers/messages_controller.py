from django.shortcuts import render
from rest_framework.decorators import api_view
from ..services import message_service

@api_view(['POST'])
def new_message(request):
    return message_service.new_message(request)

@api_view(['GET'])
def message_content(request, message_id):
    return message_service.message_content(request, message_id)

@api_view(['DELETE'])
def delete_message(request, message_id):
    return message_service.delete_message(request, message_id)

@api_view(['DELETE'])
def delete_group_messages(request, group_id):
    return message_service.delete_group_messages(group_id)

@api_view(['PUT'])
def change_message(request, message_id):
    return message_service.change_message(request, message_id)