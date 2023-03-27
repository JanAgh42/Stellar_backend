from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupsMemberSerializer
from ..models import GroupsMember

def map_user_group(request):
    try:
        groupmember_serializer = GroupsMemberSerializer(data = request.data)
        if groupmember_serializer.is_valid():
            groupmember_serializer.save()
        
        return Response("Successful mapping", status = status.HTTP_201_CREATED)
    
    except:
        return Response("Can't map user to group", status = status.HTTP_400_BAD_REQUEST)

def group_member(request, user_id, group_id):

    usergroup = GroupsMember.objects.filter(user_id = user_id)  
    usergroup_data = usergroup.GroupsMemberSerializer(usergroup, many = True).data

    return Response('', status = status.HTTP_200_OK)

