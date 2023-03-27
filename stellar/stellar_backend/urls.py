from django.urls import path

from stellar.stellar_backend.controllers import messages_controller, usersgroups_controller
from .controllers import users_controller, groups_controller, notifications_controller

user_urls = [
    path('users/<user_id>', users_controller.get_put_user),
    path('users/', users_controller.register_user),
    path('users/auth/login', users_controller.authenticate_user)
]

group_urls = [
    path('groups/<group_id>', groups_controller.manage_single_group),
    path('groups/<user_id>/owner', groups_controller.own_groups),
    path('groups/<user_id>/all', groups_controller.all_groups),
    path('groups/', groups_controller.new_group)
]

notification_urls = [
    path('notifications/<user_id>', notifications_controller.get_notifications),
    path('notifications/<user_id>/all', notifications_controller.delete_user_notifications),
    path('notifications/<notif_id>/single', notifications_controller.delete_notification),
    path('notifications/', notifications_controller.new_notification),
    path('notifications/<group_id>/group/', notifications_controller.new_group_notification)
]

message_urls = [
    path('messages/', messages_controller.new_message),
    path('messages/<message_id>', messages_controller.message_content),
    path('messages/<group_id>/get-all', messages_controller.get_group_messages),
    path('messages/<message_id>/change', messages_controller.change_message),
    path('messages/<message_id>/delete', messages_controller.delete_message),
    path('messages/<group_id>/delete-all', messages_controller.delete_group_messages)
]

usergroup_urls = [
    path('usersgroups/', usersgroups_controller.map_user_group),
    path('usersgroups/<user_id>/member/<group_id>', usersgroups_controller.group_member)
]

urlpatterns = [
    *user_urls,
    *group_urls,
    *notification_urls,
    *message_urls,
    *usergroup_urls
]