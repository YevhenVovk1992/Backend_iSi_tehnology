from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import *

# Register your models here.
TokenAdmin.raw_id_fields = ['user']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'sender', 'thread', 'created', 'is_read')
    list_filter = ('sender', 'thread')
    list_display_links = ('text', 'id')


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'participants', 'created', 'updated')
    list_filter = ('participants', )
    list_display_links = ('id', 'participants')


admin.site.register(Message, MessageAdmin)
admin.site.register(Thread, ThreadAdmin)