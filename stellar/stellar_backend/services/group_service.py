from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupSerializer
from ..serializers import GroupsMemberSerializer
from ..models import Group
from ..models import GroupsMember

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

def own_groups(user_id):
    own_groups = Group.objects.filter(owner_id = user_id)

    own_groups_data = GroupSerializer(own_groups, many = True).data

    return Response(own_groups_data, status = status.HTTP_200_OK)

def all_groups(user_id):

    groups_ids = GroupsMember.objects.filter(user_id = user_id)
    groups_ids_data = GroupsMemberSerializer(groups_ids, many = True).data

    all_groups_data = list()
    for g in groups_ids_data:
        group = Group.objects.filter(id = g['group_id'])
        all_groups_data.append(*GroupSerializer(group, many = True).data)

    return Response(all_groups_data, status = status.HTTP_200_OK)
 
def new_group(request):
    try:
        group_serializer = GroupSerializer(data = request.data)

        if group_serializer.is_valid():
            group_serializer.save()

            return Response("Group successfully created", status = status.HTTP_201_CREATED)

    except:
        return Response("Can't create new group", status = status.HTTP_409_CONFLICT)
    