from rest_framework.decorators import api_view
from ..services import usergroup_service

@api_view(['POST'])
def add_user_to_group(request):
    return usergroup_service.add_user_to_group(request)

@api_view(['GET'])
def is_member_of_group(request, user_id, group_id):
    return usergroup_service.is_member_of_group(request, user_id, group_id)

@api_view(['DELETE'])
def delete_user_from_group(request, user_id, group_id):
    return usergroup_service.delete_user_from_group(user_id, group_id)

@api_view(['GET'])
def num_where_is_owner(request, user_id):
    return usergroup_service.num_where_is_owner(user_id)