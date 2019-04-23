from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from pages.views import *

urlpatterns = [
  url(r'^$', top_level, name='top_level'),
  url(r'^cleared/(?P<episode>[\w-]+)/$', top_level_cleared, name='top_level_cleared'),
  url(r'^get_rt_api_key_handler/$', get_rt_api_key_handler, name='get_rt_api_key_handler'),
  url(r'^change_set_handler/$', change_set_handler, name='change_set_handler'),
  url(r'^set_pulse_goal_handler/$', set_pulse_goal_handler, name='set_pulse_goal_handler'),
] 

