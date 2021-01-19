# Infinite-Plex-Autoplay

Note:  This works with Roku TVs using the Plex app.  I'll update it at some point to add Chromecast functionality (1/19/2021, let's aim for before 2022 huh)

A script using the Python PlexAPI to keep Plex from killing your stream after two hours

To use this script, you'll need:

* Plexapi.  Make sure you download it from [Git](https://github.com/pkkid/python-plexapi) and NOT with pip, the version on pip is outdated.  I learned this after trying to use it for roughly six hours before finding a post somewhere saying not to use it.  Don't be me.
* Get a Plex token if you don't have one already.  See Plex's web page for more details:  https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
* Add your Plex server's URL
* Add your your TV / device name
* Add the library section and the show name.   Execute "plex.clients()" in your Python shell to pull the device names.  

The device needs to already have a connection to Plex in order for this to work, so pull up any old video and then run the script.  

There are a couple issues, I'm not great at programming so I don't understand them 100%.  Sometimes the variable for the TV show throws an XML parsing error, sometimes it doesn't.  Sometimes the timeline doesn't get pulled right.  But overall it works.

Feel free to customize for your own ends, this is pretty simple and not very pretty, but it gets the job done.

# GUI Version
This is pretty unpolished, it's a WIP.  Relies on PySimpleGUI.
