from rest_framework.decorators import api_view
from ..services import user_service

@api_view(['GET', 'PUT'])
def get_put_user(request, user_id):

    if request.method == 'GET':
        return user_service.get_user(user_id)
    
@api_view(['POST'])
def register_user(request):
    return user_service.register_user(request)

@api_view(['POST'])
def authenticate_user(request):
    return user_service.authenticate_user(request)