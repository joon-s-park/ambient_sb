from django.contrib import admin
from .models import *

class SMUserAdmin(admin.ModelAdmin):
  list_display = ['url_name', 'active_storyboard_id']

class StoryboardAdmin(admin.ModelAdmin):
  list_display = ['user', 'storyboard_id', 'current_episode']


admin.site.register(SMUser, SMUserAdmin)
admin.site.register(Storyboard, StoryboardAdmin)
