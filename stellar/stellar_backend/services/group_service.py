from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupSerializer
from ..models import Group

def get_group(group_id):
    try:
        group = Group.objects.get(id = group_id)

        group_data = GroupSerializer(group).data

    except ObjectDoesNotExist:
        return Response("Group not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(group_data, status = status.HTTP_200_OK)

def delete_group(group_id):
    try:
        group = Group.objects.get(id = group_id)

        group.delete()
    except ObjectDoesNotExist:
        return Response("Group not found", status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)

def change_group(request, group_id):
    try:
        old_group = Group.objects.get(id = group_id)
        updated_group = GroupSerializer(old_group, data = request.data)

        if updated_group.is_valid():
            updated_group.save()

            return Response(status = status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response("Group not found", status = status.HTTP_404_NOT_FOUND)
