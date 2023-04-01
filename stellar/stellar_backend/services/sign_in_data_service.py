from django.http import QueryDict

from ..serializers import SignInSerializer
from ..models import SignInData
from..helpers.service_helpers import generate_hash

import bcrypt

def create_register_entry(request, user_id):
    if isinstance(request.data, QueryDict):
        request.data._mutable = True

    request.data["user_id"] = user_id
    request.data["password"] = generate_hash(request.data["password"])

    signin_serializer = SignInSerializer(data = request.data)

    if signin_serializer.is_valid():
        signin_serializer.save()

def validate_auth(data):
    auth = SignInData.objects.get(email = data["email"])

    if auth != None:
        auth_data = SignInSerializer(auth).data
        pw_bytes = data["password"].encode("utf-8")

        if bcrypt.checkpw(pw_bytes, auth_data["password"].encode("utf-8")):
            return auth_data
        else:
            return None

    return auth