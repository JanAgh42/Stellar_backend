from rest_framework.decorators import api_view
from ..services import group_service

@api_view(['GET', 'PUT', 'DELETE'])
def manage_single_group(request, group_id):

    if request.method == 'GET':    
        return group_service.get_group(group_id)
    elif request.method == 'DELETE':
        return group_service.delete_group(group_id)