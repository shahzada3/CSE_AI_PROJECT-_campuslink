from django.contrib import admin
from .models import Group, GroupMessage

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'creator', 'member_count', 'created_at']

@admin.register(GroupMessage)
class GroupMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'timestamp']