from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from rest_framework import status
from rest_framework.response import Response

from ..serializers import GroupsMemberSerializer
from ..models import GroupsMember

def map_user_group(request):
    try:
        groupsmember_serializer = GroupsMemberSerializer(data = request.data)

    except:
        return Response("", status = status.HTTP_400_BAD_REQUEST)
    
    return Response('', status = status.HTTP_201_CREATED)

def group_member(request, user_id, group_id):
    try:
        usergroup = GroupsMember.objects.get(user_id = user_id, group_id = group_id)

    except:
        return Response("", status = status.HTTP_404_NOT_FOUND)
    
    return Response('', status = status.HTTP_200_OK)

