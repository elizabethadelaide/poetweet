import re
import json

from django.core.management.base import BaseCommand

from bot.models import Stanzas

'''
Populates database
from Files'''

def serialize(obj):
    """JSON serializer for objects not serializable by default json code"""

    return obj.__dict__

class ParseOut:

    def __init__(self):

        self.mydataobj = []

        self.lineCounter = 0
        self.stanCounter = 0

        #TODO: Change!!!!
        self.filename = "poetry.txt"

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

    def parseString(self, line, numRecursions=0):
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
            #print(d)

            stan = Stanzas(file=self.filename, \
                stanzas=d['stanza'], \
                line=d['line'], \
                text=d['text'], \
                length=len(d['text']))
            print(stan.text)
            #print(Stanzas.objects)
            print(stan.id) #test first
            stan.save()
            print(stan.id)

    def getJson(self):
        data = json.dumps(self.mydataobj, default=serialize)
        return data

#This code is placed in the management/commands folder
#run python manage.py parser
#It will run this class:
class Command(BaseCommand):
    #TODO: Add args for which files
    help = "Import file for data"
    args = "filenames, not implemented will default to poetry.txt"

    def _run_parser(self):
        po = ParseOut()
        #>:(
        filename = "/home/liz/Programs/jay_bot/jade_odd/bot/management/commands/poetry.txt"
        with open(filename) as f:
            print(f)
            po.poetry_parser(f)
        #print(po.getJson())
        po.writeJsonLineByLine()

    #what runs?
    def handle(self, *args, **options):
        self._run_parser()


if __name__=="__main__":
    po = ParseOut()
    filename = "poetry.txt"
    with open(filename) as f:
        po.poetry_parser(f)
    #print(po.getJson())
    po.writeJsonLineByLine()
