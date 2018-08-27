from rest_framework import generics
#from .serializers import StanzaslistSerializer
from .models import Stanzas, filenames
from .serializers import StanzaslistSerializer, FilenameslistSerializer
from django.contrib.auth.models import User
from rest_framework import generics

from .parser import ParseOut

from random import randint

from django.shortcuts import render
from django.template.loader import render_to_string

try:
  from HTMLParser import HTMLParser
except ImportError:
  from html.parser import HTMLParser
import logging
import re
import requests
import sys
import time
import tweepy
from config import *

'''

Twitter utils

'''

#Basic tweeting utils:
class TwitterPost(object):
  def __init__(self, auth):
    self.api = tweepy.API(auth)
  def post_tweet(self, status):
    self.api.update_status(status)

# exceptions
class TweetTooLong(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class NoValidResponse(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
html_parser = HTMLParser()
logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)


#View displays database info
#Allows import of individual stanzas
class CreateView(generics.ListCreateAPIView):
    queryset = Stanzas.objects.all()
    serializer_class = StanzaslistSerializer

    '''def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = StanzaslistSerializer(queryset, many=True)
        return Response(serializer.data)'''

    def perform_create(self, serializer):
        """Save the post data when creating a new bucketlist."""
        serializer.save()

#Test tweets
#Will update to show next tweet
def TweetView(request):
    #t = loader.get_template('bot/stanzas_list.html')
    #c = {'tweet_list': Stanzas.objects.all()}
    if (request.GET.get('sendbtn')):
        print("Button!")
        print(str(request.GET.get('mytweet')))
        status = str(request.GET.get('mytweet'))
        ta = TwitterPost(auth)
        try:
            ta.post_tweet(status)
            print(status)
        except Exception as e:
            logging.error(e)

    if (request.GET.get('refreshbtn')):
        totallength = 0
        text = ''
        keepadding = True
        while (keepadding):
            newTweet = getRandomTweet()
            textlength = newTweet.length
            textB = newTweet.text
            if (text != ''):
                print(textB[0], text[-1])
                if (textB[0] != ' ' and text[-1] != ' '):
                    textB = ' ' + textB

            if (totallength + textlength > 280):
                keepadding = False
            elif (totallength > 0 and randint(0, 2) == 1):
                keepadding = False # sometimes just make a short post
            else:
                text = text + textB
                totallength = len(text)
        context = {'text': text, 'charlength': totallength}
        print(context)
        rendered = render(request, 'tweet.html', context)
        return rendered


    rendered = render(request, 'tweet.html', {'text': 'honestly bees R sexy and seinfeld was right python send tweet'})
    return rendered

def getRandomTweet():
    queryset = Stanzas.objects .all()
    length = len(queryset)
    myid = randint(0, length-1)
    value = Stanzas.objects.get(id=myid)
    return value
