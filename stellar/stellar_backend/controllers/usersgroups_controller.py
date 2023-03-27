from rest_framework.decorators import api_view
from ..services import usergroup_service

@api_view(['POST'])
def map_user_group(request):
    return usergroup_service.map_user_group(request)

@api_view(['GET'])
def group_member(request, user_id, group_id):
    return usergroup_service.group_member(request, user_id, group_id)