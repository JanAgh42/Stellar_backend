from django.core.exceptions import ObjectDoesNotExist

from ..serializers import SessionSerializer
from ..helpers.service_helpers import generate_token, token_date, get_time
from ..models import SessionToken

def create_user_token(user_id):
    session_serializer = SessionSerializer(data = {
        "user_id": user_id,
        "token": generate_token()
    })

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

def is_token_valid(header):
    try:
        session_token = SessionToken.objects.get(user_id = header['HTTP_USER'], token = header['HTTP_TOKEN'])

        if session_token.date < get_time():
            session_token.delete()
            return False
        
        new_token = SessionSerializer(session_token).data
        new_token["date"] = token_date()

        updated_token = SessionSerializer(session_token, data = new_token)

        if updated_token.is_valid():
            updated_token.save()

            return True
    except (ObjectDoesNotExist, KeyError):
        pass
    return False