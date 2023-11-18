from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupSerializer
from ..models import Group, GroupsMember
from ..static import constants as const

from .message_service import delete_group_messages
from .usergroup_service import delete_user_from_group, add_user_to_group

def get_group(group_id):
    try:
        group = Group.objects.get(id = group_id)

        group_data = GroupSerializer(group).data

    except ObjectDoesNotExist:
        return Response(const.GROUP_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
    return Response(group_data, status = status.HTTP_200_OK)

def delete_group(group_id):
    try:
        group = Group.objects.get(id = group_id)
        
        delete_user_from_group(group.owner_id, group_id)
        delete_group_messages(group_id)

        group.delete()
    except ObjectDoesNotExist:
        return Response(const.GROUP_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)

def change_group(request, group_id):
    try:
        old_group = Group.objects.get(id = group_id)
        updated_group = GroupSerializer(old_group, data = request.data)

        if updated_group.is_valid():
            updated_group.save()

            return Response(status = status.HTTP_204_NO_CONTENT)
    except ObjectDoesNotExist:
        return Response(const.GROUP_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)


def get_own_groups(user_id):
    own_groups = Group.objects.filter(owner_id = user_id)

    own_groups_data = GroupSerializer(own_groups, many = True).data

    return Response(own_groups_data, status = status.HTTP_200_OK)

def get_all_groups(user_id):

    groups_ids = GroupsMember.objects.filter(user_id = user_id).only('group_id')

    all_groups_data = list()
    
    for id in groups_ids:
        group = Group.objects.get(id = id.group_id)
        all_groups_data.append(GroupSerializer(group).data)

    return Response(all_groups_data, status = status.HTTP_200_OK)

def search_groups(request):
    category = request.GET['category'] if 'category' in request.GET else None
    name = request.GET['name'] if 'name' in request.GET else None

    groups = Group.objects.all() if category == None else Group.objects.filter(category = category)
    groups = [group for group in groups if name in group.name or group.name in name]

    groups_data = GroupSerializer(groups, many = True).data

    return Response(groups_data, status = status.HTTP_200_OK)



def new_group(request):
    try:
        group_serializer = GroupSerializer(data = request.data)

        if group_serializer.is_valid():
            group = group_serializer.save()

            add_user_to_group({
                "user_id": group.owner_id,
                "group_id": str(group.id),
                "is_owner": True
            })

            return Response(const.GROUP_CREATED, status = status.HTTP_201_CREATED)
    except DatabaseError:
        return Response(const.GROUP_EXISTS, status = status.HTTP_409_CONFLICT)
    