from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
import random
from time import sleep
from os import system,name,path
from telegram.ext import Updater, CommandHandler
import requests
import PySimpleGUI as sg
import os
import signal
import psutil
import subprocess
from json import (load as jsonload, dump as jsondump)

SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {'Plex Token': ""}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {'Plex Token': '-PlexToken-','Plex Server URL': '-PlexURL-'}
baseurl = ''
token = ''
plex = PlexServer(baseurl, token)   
chosen_section=""

client_list = [f.title for f in plex.clients()]
section_text = [f.title for f in plex.library.sections()]
menu_def = [
            ['&File', ['&Open     Ctrl-O', '&Save       Ctrl-S', '&Properties', 'E&xit']],
            ['&Edit', ['&Paste', ['Special', 'Normal', ], 'Undo'], ],
            ['&Toolbar', ['---', 'Command &1', 'Command &2',
                          '---', 'Command &3', 'Command &4']],
            ['&Help', '&About...'], ]

sg.theme('DarkAmber')
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
        
def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except Exception as e:
        sg.popup_quick_message(f'exception {e}', 'No settings file found... will create one for you', keep_on_top=True, background_color='red', text_color='white')
        settings = default_settings
        save_settings(settings_file, settings, None)
    return settings

def save_settings(settings_file, settings, values):
    if values:
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception as e:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)

    sg.popup('Settings saved')

window, settings = sg.Window(
    'Infinite Plex',
    layout,
    default_element_size=(12, 1),
    default_button_element_size=(12, 1),
), load_settings(SETTINGS_FILE, DEFAULT_SETTINGS )

def create_settings_window(settings):
    sg.theme('DarkAmber')
    def TextLabel(text): return sg.Text(text+':', justification='r', size=(15,1))
    layout = [  [sg.Text('Settings', font='Any 15')],
                [TextLabel('Plex Token'),sg.Input(key='-PlexToken-')],
                [TextLabel('Plex Server URL'),sg.Input(key='-PlexURL-')],
                [sg.OK()]
            ]
    window = sg.Window('Settings', layout, keep_on_top=True, finalize=True)
    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception as e:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')
    return window
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    elif event == 'clients_list':
        window.FindElement('sections_list').Update(values=section_text)
    elif event == 'sections_list':
        chosen_section = values['sections_list']
        shows = plex.library.section(chosen_section).all()
        num = len(shows)
        shownames = []
        i=0
        for i in range(0,num):
            shownames.append(shows[i].title)
        window.FindElement('shows_list').Update(values=(shownames))
    elif event == 'shows_list':
        chosen_section = values['sections_list']
        chosen_show = values['shows_list']
        episodes = plex.library.section(chosen_section).get(chosen_show).episodes()
        num = len(episodes)
        episodenames = []
        i=0
        for i in range(0,num):
            episodenames.append(episodes[i].title)
        window.FindElement('episodes_list').Update(values=(episodenames))
    elif event == 'Properties':
        event, values = create_settings_window(settings).read(close=True)
        if event == 'OK':
            window.close()
            window = None
            save_settings(SETTINGS_FILE, settings, values)
    elif event == 'start_autoplay': 
        while(1):
            clienttext = values['clients_list']
            chosen_section = values['sections_list']
            chosen_show = values['shows_list']
            client = plex.client(clienttext)
            new = plex.library.section(chosen_section).get(chosen_show).episodes()[random.randint(1,91)]
            client.playMedia(new)
            print(client.timeline)
            sg.popup("Starting "+new.title)
            sleep(60)
            total = (client.timeline.duration/1000)
            watched = (client.timeline.time/1000)
            end = ((total - watched) - 1)
            print("Sleeping for ", end/60, "minutes")
            requests.post(telegrammsg + "Starting a new episode")
            sleep(end)
