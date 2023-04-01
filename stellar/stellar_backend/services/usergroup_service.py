from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupsMemberSerializer
from ..models import GroupsMember, Group, User
from ..static import constants as const

from .notification_service import new_notification

def add_user_to_group(data):
    try:
        groupmember_serializer = GroupsMemberSerializer(data = data)

        if groupmember_serializer.is_valid():
            groupmember_serializer.save()

            group_owner = Group.objects.get(id = data["group_id"]).only('owner_id', 'name')
            new_member_name = User.objects.get(id = data["user_id"]).name

            if group_owner.owner_id != data["user_id"]:
                new_notification({
                    "user_id": group_owner.owner_id,
                    "message": const.JOINED_GROUP.format(new_member_name, group_owner.name)
                })
        
            return Response(const.UG_CREATED, status = status.HTTP_201_CREATED)
    
    except DatabaseError:
        return Response(const.UG_INVALID, status = status.HTTP_400_BAD_REQUEST)
    
def delete_user_from_group(user_id, group_id):
    try:
        usergroup = GroupsMember.objects.get(user_id = user_id, group_id = group_id)
        usergroup.delete()

        group_owner = Group.objects.get(id = group_id).only('owner_id', 'name')
        new_member_name = User.objects.get(id = user_id).name

        if group_owner.owner_id != user_id:
            new_notification({
                "user_id": group_owner.owner_id,
                "message": const.LEAVE_GROUP.format(new_member_name, group_owner.name)
            })

        return Response(status = status.HTTP_204_NO_CONTENT)

    except ObjectDoesNotExist:
        return Response(const.UG_NOT_FOUND, status = status.HTTP_404_NOT_FOUND)
    
    

def is_member_of_group(user_id, group_id):
    try:
        GroupsMember.objects.get(user_id = user_id, group_id = group_id)

    except ObjectDoesNotExist:
        return Response({"is_member": False}, status = status.HTTP_200_OK)
    
    return Response({"is_member": True}, status = status.HTTP_200_OK)

def num_where_is_owner(user_id):
    groups = GroupsMember.objects.filter(user_id = user_id)
    groups_data = GroupsMemberSerializer(groups, many = True).data
    num_is_owner = 0

    for group in groups_data:
        if group["is_owner"] == True:
            num_is_owner += 1

    return Response({"num_groups_owner": num_is_owner}, status = status.HTTP_200_OK)


