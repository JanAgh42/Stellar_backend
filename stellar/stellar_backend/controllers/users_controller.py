from django.shortcuts import render
from rest_framework.decorators import api_view
from ..services import user_service, session_service, sign_in_data_service

@api_view(['GET', 'PUT'])
def get_put_user(request, user_id):

    if request.method == 'GET':
        return user_service.get_user(user_id)
    
@api_view(['POST'])
def create_user(request):
    return user_service.register_user(request)