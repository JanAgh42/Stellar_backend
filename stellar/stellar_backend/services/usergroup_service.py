from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupsMemberSerializer
from ..models import GroupsMember

def add_user_to_group(request):
    try:
        groupmember_serializer = GroupsMemberSerializer(data = request.data)
        if groupmember_serializer.is_valid():
            groupmember_serializer.save()
        
        return Response("User added to group", status = status.HTTP_201_CREATED)
    
    except:
        return Response("Invalid group or user id", status = status.HTTP_400_BAD_REQUEST)
    
def delete_user_from_group(user_id, group_id):
    try:
        usergroup = GroupsMember.objects.get(user_id = user_id, group_id = group_id)
        usergroup.delete()

    except ObjectDoesNotExist:
        return Response("User is not a member of this group", status = status.HTTP_404_NOT_FOUND)
    
    return Response(status = status.HTTP_204_NO_CONTENT)


def is_member_of_group(request, user_id, group_id):
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


