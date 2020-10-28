from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
from plexapi.playqueue import PlayQueue
from time import sleep
from os import system,name,path
from telegram.ext import Updater, CommandHandler
import requests
import PySimpleGUI as sg
import signal
import psutil
import subprocess
from json import (load as jsonload, dump as jsondump)
import logging

#Notes
#If script crashes with an XML parsing error, restart your device, then log back into Plex on the device.

#Plex Conf
baseurl = ''
token = ''
plex = PlexServer(baseurl, token)
media_choice = ["","",""]
section_choice = ""
show_choice = ""
episode_choice = ""
episodes_full = []
episodenames = []
shownames = []
shows_full = []
#Initial data pull
client_list = [f.title for f in plex.clients()]
client = ""
section_text = [f.title for f in plex.library.sections() if "TV" in str(f)]
#Top menu definition
menu_def = [
            ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Toolbar', ['---', 'Command &1', 'Command &2',
                          '---', 'Command &3', 'Command &4']],
            ['&Help', '&About...'], ]

sg.theme('DarkAmber')
#Configure logging, but doesn't seem to do much...
logging.basicConfig(
     level=logging.DEBUG, 
     format= '[%(asctime)s] (%(pathname)s:%(lineno)d) %(levelname)s - %(message)s',
     datefmt='%H:%M:%S'
 )


#GUI Layout
layout = [  
            [sg.Menu(menu_def, tearoff=False, pad=(200, 1))],
            [sg.Text('Client: '),sg.Combo(values=client_list, size=(35, 30),key="clients_list",enable_events=True)],  #Clients
            [sg.Text('Library: '),sg.Combo(values="", size=(35, 30),key="sections_list",enable_events=True)],  #Sections
            [sg.Text('Show: '),sg.Combo(values="", size=(35, 30),key="shows_list",enable_events=True)],  #Shows
            [sg.Text('Episode: '),sg.Combo(values="", size=(35, 30),key="episodes_list",enable_events=True)],  #Episodes
            [sg.Text('Infinite Plex Autoplay.')],
            [sg.Button('Start', button_color=('green', 'black'),key='start_autoplay')],
            [sg.Button('Stop', button_color=('green', 'black'),key='stop_autoplay')]
        ]      

#GUI
window = sg.Window(
    'Infinite Plex',
    layout,
    default_element_size=(12, 1),
    default_button_element_size=(12, 1),
)

def showTimeProgress():
    currentupdate = "placeholder"
    client.timelines()
    firsttimeline = client.timeline
    if firsttimeline == None:
        print("Waiting for a timeline to generate...")
        while firsttimeline == None:
            sleep(1)
            firsttimeline = client.timeline
    total = client.timeline.duration/1000
    while (client.timeline.time/1000) < total:
        watched = (client.timeline.time/1000)
        sg.OneLineProgressMeter('My 1-line progress meter', watched, total, 'single')

#Main GUI event listener
while True:
    sg.popup("Still a work in progress!")
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

    elif event == 'clients_list':
        window.FindElement('sections_list').Update(values=section_text)
        client = plex.client(values['clients_list'])
        
    elif event == 'sections_list':
        section_choice = values['sections_list']
        shows = plex.library.section(section_choice).all()
        i=0
        for i in range(0,len(shows)):
            shownames.append(shows[i].title)
            shows_full.append(shows[i])
        window.FindElement('shows_list').Update(values=(shownames))

    elif event == 'shows_list':
        show_choice = values['shows_list']
        showseasons = plex.library.section(section_choice).get(show_choice)
        get_episodes = plex.library.section(section_choice).get(show_choice).episodes()
        i=0
        for i in range(0,len(get_episodes)):
            episodenames.append(get_episodes[i].title)
            episodes_full.append(get_episodes[i])
        window.FindElement('episodes_list').Update(values=(episodenames))
        
    elif event == 'episodes_list':
        episode_choice = values['episodes_list']

    elif event == 'start_autoplay': 
        client.playMedia(showseasons.episode(episode_choice))
        showTimeProgress()
