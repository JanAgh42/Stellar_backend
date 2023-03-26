from django.urls import path
from .controllers import users_controller, groups_controller

urlpatterns = [
    path('users/<user_id>', users_controller.get_put_user),
    path('users/', users_controller.register_user),
    path('users/auth/login', users_controller.authenticate_user),
    path('groups/<group_id>', groups_controller.manage_single_group)
]