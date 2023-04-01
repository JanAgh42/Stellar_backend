from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from ..services import user_service, session_service
from ..static import constants as const

@api_view(['GET', 'PUT'])
def get_put_user(request, user_id):
    if not session_service.is_token_valid(request.META):
        return Response(const.INVALID_TOKEN, status = status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        return user_service.get_user(user_id)
    elif request.method == 'PUT':
        return user_service.change_user(request, user_id)
    
@api_view(['POST'])
def register_user(request):
    return user_service.register_user(request)

@api_view(['POST'])
def authenticate_user(request):
    return user_service.authenticate_user(request)