from django.core.exceptions import ObjectDoesNotExist
from django.http import QueryDict

from ..serializers import SessionSerializer
from ..helpers.service_helpers import generate_token
from ..models import SessionToken

def create_user_token(user_id):
    
    data = QueryDict()
    data._mutable = True

    data.update({
        "user_id": user_id,
        "token": generate_token()
    })

    session_serializer = SessionSerializer(data = data)

    if session_serializer.is_valid():
        token = session_serializer.save()

        return str(token.token)
    return None

def get_user_token(user_id):
    try:
        token = SessionToken.objects.get(user_id = user_id)
        
        return SessionSerializer(token).data["token"]
    except ObjectDoesNotExist:
        return create_user_token(user_id)