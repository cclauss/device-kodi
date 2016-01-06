import xbmc
import xbmcaddon

import os
import inspect
import uuid
import logging

cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"lib")))
if cmd_subfolder not in sys.path:
	sys.path.insert(0, cmd_subfolder)
		
import ibmiotf.device

def commandProcessor(cmd):
	global pollInterval
	print("Command received: %s" % cmd.data)
	if cmd.command == "setInterval":
		if 'interval' not in cmd.data:
			print("Error - command is missing required information: 'interval'")
		else:
			pollInterval = cmd.data['interval']
			iotfAddon.setSetting('iotfinterval', pollInterval)
	elif cmd.command == "pause":
		xbmc.Player().pause()
	elif cmd.command == "stop":
		xbmc.Player().stop()
	


# Look up the device configuration
iotfAddon = xbmcaddon.Addon()

organization = iotfAddon.getSetting('iotforgid')
deviceType = "kodi"
deviceId = iotfAddon.getSetting('iotfdeviceid')
authMethod = "token"
authToken = iotfAddon.getSetting('iotfauthtoken')

pollInterval = iotfAddon.getSetting('iotfinterval')


fhFormatter = logging.Formatter('%(asctime)-25s %(name)-25s ' + ' %(levelname)-7s %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(fhFormatter)
ch.setLevel(logging.DEBUG)
			
# Initialize the device client.
try:
	deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
	deviceCli = ibmiotf.device.Client(deviceOptions, logHandlers=ch)
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()

deviceCli.commandCallback = commandProcessor
deviceCli.connect()
player = xbmc.Player()

# See: http://wiki.xbmc.org/index.php?title=HOW-TO:Automatically_start_addons_using_services
while (not xbmc.abortRequested):
	# Polling implementation ... would be better if we could subscribe to change notifications
	playerData = {}
	
	# Determine what (if anything) is playing and it's type
	playerData['playing'] = (player.isPlaying() == 1)  	# Is user watching a video?
	
	if playerData['playing']:
		if player.isPlayingVideo():
			playerData['contentType'] = "video"
			
			videoTag = player.getVideoInfoTag()
			
			castArray = videoTag.getCast().split("\n")
			if len(castArray) > 0:
				playerData['info'] = {'cast': castArray}
			playerData['info']['director'] = videoTag.getDirector()
			playerData['info']['file'] = videoTag.getFile()
			playerData['info']['firstAired'] = videoTag.getFirstAired()
			playerData['info']['genre'] = videoTag.getGenre()
			playerData['info']['imdbNumber'] = videoTag.getIMDBNumber()
			playerData['info']['lastPlayed'] = videoTag.getLastPlayed()
			playerData['info']['originalTitle'] = videoTag.getOriginalTitle()
			playerData['info']['path'] = videoTag.getPath()
			playerData['info']['pictureUrl'] = videoTag.getPictureURL()
			playerData['info']['playCount'] = videoTag.getPlayCount()
			playerData['info']['plot'] = videoTag.getPlot()
			playerData['info']['plotOutline'] = videoTag.getPlotOutline()
			playerData['info']['premiered'] = videoTag.getPremiered()
			playerData['info']['rating'] = videoTag.getRating()
			playerData['info']['tagline'] = videoTag.getTagLine()
			playerData['info']['title'] = videoTag.getTitle()
			playerData['info']['votes'] = videoTag.getVotes()
			playerData['info']['credits'] = videoTag.getWritingCredits()
			playerData['info']['year'] = videoTag.getYear()
			
			
		elif player.isPlayingAudio():
			playerData['contentType'] = "audio"
			playerData['info'] = player.getMusicInfoTag()
		elif player.isPlayingRDS():
			playerData['contentType'] = "rds"
		
		try:
			playerData['file'] = player.getPlayingFile()
		except:
			# We may not be playing an actual file
			pass
			
		playerData['time'] = player.getTime()
		playerData['totalTime'] = player.getTotalTime()
	
	print(playerData)
	success = deviceCli.publishEvent("player", "json", playerData, qos=0)
	xbmc.sleep(pollInterval * 1000)


# We are shutting down, disconnect
print("Beginning shut down")
deviceCli.disconnect()

