from django.db import models
from django.contrib.auth.models import User

import re
import json
import os

#Start with basic:
class filenames(models.Model):
    name = models.CharField(max_length=120)
    added = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class RawInput(models.Model):
    #filename
    file = models.CharField(max_length=200)
    #fulltext, long
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)
    date_modified = models.DateTimeField(auto_now=True)



class Stanzas(models.Model):
    #file poem is from
    file = models.CharField(max_length=200)
    #Stanza
    stanzas = models.IntegerField(default=0)
    #Line number
    line = models.IntegerField(default=0)
    #Text
    text = models.CharField(max_length=280)
    #Length
    length = models.IntegerField(default=0)
    #when the poem was added
    date_added = models.DateTimeField(auto_now=True)
    #if the stanza was modified
    date_modified = models.DateTimeField(auto_now=True)
    #When the poem was last posted
    date_posted_last = models.DateTimeField(auto_now=True)
