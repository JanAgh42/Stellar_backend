from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

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
    try:

        groups_ids = GroupsMember.objects.filter(user_id = user_id)
        # all_groups_data = None
        # for group in groups_ids:
        data = GroupsMemberSerializer(groups_ids, many=True).data
    except DatabaseError:
        print(DatabaseError)
    return Response("boo", status = status.HTTP_200_OK)
    # own_groups_data = GroupSerializer(own_groups, many = True).data

    # return Response(own_groups_data, status = status.HTTP_200_OK)
    