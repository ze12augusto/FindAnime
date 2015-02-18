#!/usr/bin/python

import sys, getopt
import os
import anitube
from config import Config

def usage(exitCode):
	print("findAnime.py -n <anime's name>")
	print("or")
	print("findAnime.py -n <anime's name> -s <server to search>")
	sys.exit(exitCode)


def getServerDefault():
	return getServerFromAgrvs("Anitube")


def getServerFromAgrvs(serverName):
	if "Anitube" in serverName:
		return  { "name" : "Anitube", "host" : "http://anitube.xpg.uol.com.br/search/?search_id=" }
	else:
		print("Invalid server")
		sys.exit(2)


def checkArgv(argv):
	__args__ = {}
	if len(argv) == 0:
		usage(2)
	try:
		opts, args = getopt.getopt(argv,"hn:s:",["name=","server="])
	except getopt.GetoptError:
		usage(2)
	for opt, arg in opts:
		if opt == '-h':
			usage(1)
		elif opt in ("-n", "--name"):
			__args__["name"] = arg.replace(" ", "+")
		elif opt in ("-s", "--server"):
			__args__["server"] = arg

	if "name" not in __args__:
		usage(2)
	return __args__


def main(argv):
	anime = checkArgv(argv)
	Config.animesWasFoundPrevious(anime)
	server = getServerDefault()
	if "server" in anime:
		server = getServerFromAgrvs(anime["server"])
	anitube.searchForAnime(server, anime)


if __name__ == "__main__":
	if not os.path.exists( Config.getConfigFolder() ):
		os.makedirs( Config.getConfigFolder() )
	main(sys.argv[1:])