import json
import os
import datetime
import pytz
import random, string
import re

from django.conf import settings
from django.http import Http404
from django.template import RequestContext
from datetime import date

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.template.loader import render_to_string
from django.template.context import RequestContext
from django.shortcuts import (render, redirect, HttpResponse, 
                              render_to_response, get_object_or_404, 
                              HttpResponseRedirect)

from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount

from ambient_sb.settings import BASE_DIR
from .models import * 
from .rescuetime_api import *

STATIC_URL = settings.STATIC_URL
no_auth_background = STATIC_URL + 'img/set_1/full/27.png'

def is_ascii(str):
  """ Checks to see if the given string is in ascii 

  Args:
      str: string in question 

  Returns:
      True if it is, and False otherwise. 
  """
  return True


def get_random_string(len):
    """ get random string in all lowercase

    Args:
        len: desired length of the string 

    Returns:
        randomly generated string
    """
    return (''.join(random.choice(string.ascii_lowercase) for i in range(len)))


@receiver(user_signed_up)
def sign_up_receiver(sender, **kwargs):
  """Sets up user account upon registration. 

  Called when a new user is signed up. This is where user's 
  'url_name' is set. It recieves the signal from allauth 
  application using Facebook as its provider. 
  
  (NOTE: as of Aug 7th, 2016, we only support Facebook login. Some
  part of the code below may be based on the assumption that we use 
  Facebook as the authentification provider. That is, in case we 
  may want to include other ways of logging in, we need to make more
  sophisticated ways of making sure that url_name remains unique.)

  User's 'url_name' has to be unique. 

  Args:
      sender
      kwargs
  """
  user = kwargs.pop('user')
  url_name = ""

  if is_ascii(user.first_name) and is_ascii(user.last_name):
      if user.first_name: 
          url_name += user.first_name.replace(" ", "")
      if user.last_name: 
          url_name += user.last_name.replace(" ", "")
      if not user.first_name and not user.last_name: 
          url_name += get_random_string(15)
  else: 
      url_name += get_random_string(15)

  pre_url_name = url_name

  # Check if url_name already exists. 
  url_name_already_exists = (SMUser.objects
                             .filter(url_name=url_name).exists())
  # If url_name already exists, add 9 to username_number until we 
  # find a unique match that we can use. 
  username_number = 1
  # emergency_exit_count. I put this emergency exit for case where
  # below while loop runs berserk and keep on going. 
  exit_count = 0
  while url_name_already_exists:
      exit_count += 1 
      if exit_count >= 20: 
          user.url_name = get_random_string(100)
          user.save()
          return
      username_number += random.randint(0, 50)
      url_name = pre_url_name + str(username_number)
      url_name_already_exists = (SMUser.objects
                                 .filter(url_name=url_name).exists())

  user.url_name = url_name
  user.save()

  sb = Storyboard.objects.create(user=user, storyboard_id=1, current_episode=1)
  sb.save()


def return_all_episode_thumbnail(user):
  current_sb = Storyboard.objects.filter(user=user, storyboard_id=user.active_storyboard_id)
  all_thumbnail = []
  try:
    if user.active_storyboard_id == 1: 
      current_episode = current_sb[0].current_episode/3
      for i in range (10): 
        if current_episode-1 > i:
          all_thumbnail += [STATIC_URL + 'img/set_1/thumbnail/' + str(i+1)  + '.png']
        else: 
          all_thumbnail += [STATIC_URL + 'img/unknown_episode.png']
    elif user.active_storyboard_id == 2: 
      current_episode = current_sb[0].current_episode/4
      for i in range (20): 
        if current_episode-1 > i:
          all_thumbnail += [STATIC_URL + 'img/set_2/thumbnail/' + str(i+1)  + '.jpg']
        else: 
          all_thumbnail += [STATIC_URL + 'img/unknown_episode.png']
  except: 
    pass
  return all_thumbnail


def return_curr_episode(user, episode_number): 
  if episode_number == -1:
    current_sb = Storyboard.objects.filter(user=user, storyboard_id=user.active_storyboard_id)
    episode = ""
    try:
      current_episode = current_sb[0].current_episode
      if user.active_storyboard_id == 1: 
        episode = STATIC_URL + 'img/set_1/full/' + str(current_episode) + '.png'
      elif user.active_storyboard_id == 2: 
        episode = STATIC_URL + 'img/set_2/full/' + str(current_episode) + '.jpg'
    except: 
      pass
    return episode
  else: 
    current_sb = Storyboard.objects.filter(user=user, storyboard_id=user.active_storyboard_id)
    episode = ""
    try:
      if user.active_storyboard_id == 1: 
        current_episode = episode_number * 3
        episode = STATIC_URL + 'img/set_1/full/' + str(current_episode) + '.png'
      if user.active_storyboard_id == 2: 
        current_episode = episode_number * 4
        episode = STATIC_URL + 'img/set_2/full/' + str(current_episode) + '.jpg'
    except: 
      pass
    return episode


def top_level_page_setup(request, episode):
  user_extra_data = None
  all_episode_thumbnail = None
  curr_episode = no_auth_background
  date_string = date.today().strftime('%A %d %B')
  new_user = False
  thumbnail_limit = 0

  if request.user.is_authenticated():
    if request.user.rt_api_key == "":
      new_user = True
    if (request.user.storyboard_last_updated.date() != datetime.datetime.now().date()):
      try: 
        productivity_pulse = get_yesterday_report(request.user.rt_api_key)['productivity_pulse']
        if productivity_pulse > request.user.pulse_goal:
          current_sb = Storyboard.objects.filter(user=user, storyboard_id=user.active_storyboard_id)
          current_sb.current_episode += 1
          current_episode.save()
        request.user.storyboard_last_updated = datetime.datetime.now()
        request.user.save()
      except: 
        pass
    user_extra_data = request.user.socialaccount_set.all()[0].extra_data
    all_episode_thumbnail = return_all_episode_thumbnail(request.user)
    curr_episode = return_curr_episode(request.user, episode)

    current_sb = Storyboard.objects.filter(user=request.user, storyboard_id=request.user.active_storyboard_id)[0]
    if request.user.active_storyboard_id == 1:
      thumbnail_limit = current_sb.current_episode / 3
    else:
      thumbnail_limit = current_sb.current_episode / 4


  context = {
    "date_string": date_string,
    "user_extra_data": user_extra_data,
    "all_episode_thumbnail": all_episode_thumbnail,
    "curr_episode": curr_episode,
    "new_user": new_user,
    "thumbnail_limit": thumbnail_limit,
  }

  return context


def top_level(request):
  episode = -1

  context = top_level_page_setup(request, episode)
  template = "pages/home/home.html"
  return render(request, template, context)


def top_level_cleared(request, episode):
  episode = int(episode)

  context = top_level_page_setup(request, episode)
  template = "pages/home/home.html"
  return render(request, template, context)




def get_rt_api_key_handler(request):
  if not request.user.is_authenticated() or not request.method == 'POST':
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  request.user.rt_api_key = str(request.POST.get('rt_api_key',None))
  request.user.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


def change_set_handler(request):
  if not request.user.is_authenticated() or not request.method == 'POST':
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  request.user.active_storyboard_id = int(request.POST.get('story_type',None))
  request.user.save()

  if not Storyboard.objects.filter(user=request.user, 
                                   storyboard_id=request.user.active_storyboard_id): 
    sb = Storyboard.objects.create(user=request.user, 
                                   storyboard_id=request.user.active_storyboard_id, 
                                   current_episode=1)
    sb.save()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 


def set_pulse_goal_handler(request):
  if not request.user.is_authenticated() or not request.method == 'POST':
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
  request.user.pulse_goal = int(request.POST.get('pulse_goal',None))
  request.user.save()

  return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 










