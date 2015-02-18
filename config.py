#!/usr/bin/python

from subprocess import Popen, PIPE, STDOUT
import codecs
import sys
import jellyfish

class Config:

	def getConfigFolder():
		return "/tmp/FindAnime"


	def executeCmdCommand(command):
		cmd = Popen( command , shell=True , stdout=PIPE , stderr=STDOUT )
		result = cmd.communicate()[0]
		result = str( result )
		return result


	def showDataFromTempFile(file_name):
		tempFile = codecs.open( Config.getConfigFolder() + "/" + file_name, "r+", "utf8" )
		utf8_text = tempFile.read( )
		tempFile.close( )
		print(utf8_text)
		sys.exit()


	def animesWasFoundPrevious(anime):
		animesName = anime["name"]
		command = "ls " + Config.getConfigFolder()
		result = Config.executeCmdCommand(command)
		result = result.split("\\n")
		for name in result:
			if animesName in name:
				Config.showDataFromTempFile(animesName)


	def write_text_on_temp_file( file_name, text ) :
		temp_file = codecs.open( Config.getConfigFolder() + "/" + file_name, "w", "utf8" )
		temp_file.write( text )
		temp_file.close( )


	def compareAnimesName(episodes, name):
		for episode in episodes:
			distance = jellyfish.levenshtein_distance(episode["name"], name)
			if distance <= 2:
				return False
		return True


	def getOnlyMostAproximateAnimesNameWithInformedName(episodes, anime):
		__episode__ = {}
		tempDistance = 100
		for episode in episodes:
			distance = jellyfish.levenshtein_distance(episode["name"], anime["name"])
			if distance < tempDistance:
				__episode__ = episode
				tempDistance = distance
		return __episode__
