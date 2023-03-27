from rest_framework.decorators import api_view
from ..services import group_service

@api_view(['GET', 'PUT', 'DELETE'])
def manage_single_group(request, group_id):

    if request.method == 'GET':    
        return group_service.get_group(group_id)
    elif request.method == 'DELETE':
        return group_service.delete_group(group_id)
    elif request.method == 'PUT':
        return group_service.change_group(request, group_id)
    
@api_view(['GET'])
def own_groups(request, user_id):
    return group_service.own_groups(user_id)

@api_view(['GET'])
def all_groups(request, user_id):
    return group_service.all_groups(user_id)

@api_view(['POST'])
def new_group(request):
    return group_service.new_group(request)