import datetime
import pytz
import os
import random
import string
import re

from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage as storage

# get custom Django settings variable here. 
from django.conf import settings
DEBUG = settings.DEBUG

class SMUser(AbstractUser):
  url_name = models.CharField(max_length=127, unique=True)
  active_storyboard_id = models.IntegerField(blank=False, null=False, default=1)
  storyboard_last_updated = models.DateTimeField(default=now, blank=False)
  rt_api_key = models.CharField(max_length=611, default="")
  pulse_goal = models.IntegerField(blank=False, null=False, default=60)

class Storyboard(models.Model): 
  user = models.ForeignKey(SMUser, blank=False, null=False)
  storyboard_id = models.IntegerField(blank=False, null=False, default=1)
  current_episode = models.IntegerField(blank=False, null=False, default=1)

