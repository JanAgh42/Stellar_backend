from django.urls import path
from .controllers import users_controller as con

urlpatterns = [
    path('users/<user_id>', con.get_put_user),
    path('users/', con.register_user),
    path('users/auth/login', con.authenticate_user)
]