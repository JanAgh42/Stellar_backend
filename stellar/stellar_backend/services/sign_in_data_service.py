from django.http import QueryDict

from ..serializers import SignInSerializer
from ..models import SignInData

def create_register_entry(request, user_id):
    if isinstance(request.data, QueryDict):
        request.data._mutable = True

    request.data["user_id"] = user_id
    signin_serializer = SignInSerializer(data = request.data)

    if signin_serializer.is_valid():
        signin_serializer.save()

def validate_auth(data):
    auth = SignInData.objects.get(email = data["email"], password = data["password"])

    if auth != None:
        return SignInSerializer(auth).data

    return auth