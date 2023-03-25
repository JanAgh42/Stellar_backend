from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Group)
admin.site.register(Notification)
admin.site.register(Message)
admin.site.register(SignInData)
admin.site.register(SessionToken)
admin.site.register(GroupsMember)
