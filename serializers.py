# api/serializers.py

from rest_framework import serializers
from .models import Stanzas, filenames, RawInput

import re
import json

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    return obj.__dict__

class ParseOut:

    def __init__(self):

        self.mydataobj = []

        self.lineCounter = 0
        self.stanCounter = 0

    #ideas on how to parse poetry
    def poetry_parser(self, f):
        """
        return JSON with
        title
        text
        line #
        stanza?
        """

        for line in f:
            self.parseString(line, 0)

    def parseString(self, line, numRecursions):
        #0: Remove new line from windows >:(
        text = re.sub(r'\u2028', '', line)
        #A: Remove leading spaces
        text = re.sub(r'^\s+', '', text)
        #B: Replace tabs with four spaces
        text = re.sub(r'\t', '    ', text)

        text = re.sub(r'\s+$', '', text)
        #C: Check if line is less than 280 Characters:
        if (len(text) > 280):
            '''print("Long text in stanza", self.stanCounter)
            print("Line number", self.lineCounter)
            print("Text is", text)'''
            if (numRecursions == 0):
                text = re.sub(r'/+', '\n/', text) # will erase double // not ideal
                text = text.split('\n')
                for t in text:
                    self.parseString(t, 1)
                return 0
            elif (numRecursions == 1):
                text = re.sub(r'\.+', '.\n', text) # will erase double // not ideal
                text = text.split('\n')
                #print(text)
                for t in text:
                    self.parseString(t, 2)
                return 0
            else:
                print("====== Error line too long ==== ")
                print("Long text in stanza", self.stanCounter)
                print("Line number", self.lineCounter)
                print("Text is", text)
                '''for t in str(list(text)(::279)):
                    parseString(t, 3)'''
                return 0

        #D: Remove Trailing white space
        text = re.sub(r'\s+$', '', text)

        if not text:
            self.stanCounter += 1 # next stanza
        else:
            self.lineCounter += 1

            self.mydataobj.append({"title":"poetry","stanza":self.stanCounter, \
                "line":self.lineCounter, "text":text})
            return 0
        #print("len(text)", len(text))
            '''print("text", text)
            print("Line #", counter)
            print("Stanza #", stanza)'''

    #Unclear if Django models does batch or how....
    def writeJsonLineByLine(self):
        for d in self.mydataobj:
            print(d)
            stan = Stanzas(d)
            print(stan.id)

    def getJson(self):
        data = json.dumps(self.mydataobj, default=serialize)
        return data

class FilenameslistSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = filenames
        fields = ('id', 'name', 'added')
        read_only_fields = ['added']

class StanzaslistSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance in JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the models fields."""
        model = Stanzas
        fields = ('id', 'file', 'stanzas', 'line', 'text', 'length', 'date_added', 'date_modified', 'date_posted_last')
        read_only_fields = ['date_added', 'date_modified', 'date_posted_last']

class RawlistSerializer(serializers.ModelSerializer):

    class Meta:
        """Meta class to map serializer's fields with the models fields."""
        model = RawInput
        fields = ('id', 'file', 'text', 'date_added', 'date_modified')
        read_only_fields = ['date_added', 'date_modified']        
