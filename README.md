# IoTF Device Client for Kodi

## Overview
This addon for Kodi syncs your current activity into the IoT Foundation and supports remote control of your device:

- [Internet of Things Foundation](https://internetofthings.ibmcloud.com)
- [Kodi](http://kodi.tv/)

## Events

### player
Every 10 seconds (the interval is configurable) the addon will publish a ``player`` event containing the following information:
- ``playing`` - True|False based on whether current media is playing.  Al other properties will only be submitted if this is True
- ``contentType`` - video|audio|rds
- ``file`` - The file currently being played 
- ``time`` - The current progress of the item being played 
- ``totalTime`` - The length of the current item being played

If the media being played is a video any information from the tag will also be included in the event:

- ``info.cast``
- ``info.director``
- ``info.file``
- ``info.firstAired``
- ``info.genre``
- ``info.imdbNumber``
- ``info.lastPlayed``
- ``info.originalTitle``
- ``info.path``
- ``info.pictureUrl``
- ``info.playCount``
- ``info.plot``
- ``info.plotOutline``
- ``info.premiered``
- ``info.rating``
- ``info.tagline``
- ``info.title``
- ``info.votes``
- ``info.credits``
- ``info.year``

## Supported Commands
Command control is currently veyr limited:

### setInterval
This command can be used to alter the frequency at which the addon will poll Kodi and report the player state to IoTF.  Expects a payload containing the new polling interval (in seconds):

```json
{
  'interval': 60
}
```

### pause
This command can be used to pause/resume the currently playing media, it does not require any payload

### stop
This command can be used to stop the currently playing media, it does not require any payload
