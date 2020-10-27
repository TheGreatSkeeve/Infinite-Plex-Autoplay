from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
import random
from time import sleep
from os import system,name
from telegram.ext import Updater, CommandHandler
import requests

baseurl = ''    #http://192.168.1.2:32400
token = ''      #xxxxxxxxxxxxxxxxxxxx
plex = PlexServer(baseurl, token)
client = plex.client("")    #TV Name

def clear():
    _ = system('cls')
while(1):
    ep=random.randint(1,91)
    new = plex.library.section("TV (Kids)").get('Blue\'s Clues').episodes()[ep]
    client.playMedia(new)
    print(client.timeline)
    print("Starting "+new.title)
    sleep(60)
    total = (client.timeline.duration/1000)
    watched = (client.timeline.time/1000)
    end = ((total - watched) - 1)
    print("Sleeping for ", end/60, "minutes")
    sleep(end)
    
    
            
