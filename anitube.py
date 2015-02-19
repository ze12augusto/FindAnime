#!/usr/bin/python

from urllib.request import urlopen
from bs4 import BeautifulSoup
from config import Config

def searchForAnime(server, anime):
	animesName = anime["name"]
	print("Searching for ", animesName, " in ", server["name"])
	response = urlopen(server["host"] + animesName)
	if response.getcode() != 200:
		print("Server dind't provide any response")
		sys.exit(2)
	html = str(response.read())
	response.close()
	__episodes__ = parseHtmlAndGetEpisodes(html)
	getAnimeForGetDescription(__episodes__, anime)


def getAnimeForGetDescription(episodes, anime):
	if len(episodes) == 0:
		print("Anime not found")
		sys.exit()
	__filtred_episodes__ = []
	for episode in episodes:
		if Config.compareAnimesName(__filtred_episodes__, episode["name"]):
			__filtred_episodes__.append(episode)
	episodeToGetDescription = Config.getOnlyMostAproximateAnimesNameWithInformedName(__filtred_episodes__, anime)
	getAnimesDescription(episodeToGetDescription["url"], anime, False)


def getAnimesDescription(url, anime, ready):
	response = urlopen(url)
	if response.getcode() != 200:
		print("Server dind't provide any response")
		sys.exit(2)
	html = str(response.read())
	response.close()
	if ready:
		parseHtmlAndGetDescription(html, anime, url)
	else:
		parseHtmlAndGetCategory(html, anime)


def parseHtmlAndGetDescription(html, anime, url):
	soup = BeautifulSoup(html)
	description = "\n\nIntroduction:\n\n\t"
	for div in soup.find_all('div'):
		if "class" in div.attrs:
			if "mainBox" in div["class"]:
				li = div.find("ul").find_all("li")[1]
				description += str(li.find("p").string)
				description += "\n\nURL:\n\n\t" + url + " \n"
				Config.write_text_on_temp_file( anime["name"], description )
				Config.showDataFromTempFile(anime["name"])
				sys.exit()


def parseHtmlAndGetCategory(html, anime):
	soup = BeautifulSoup(html)
	div = soup.find(id="fragment-1")
	for li in div.find_all("li"):
		if "viewVideoDetail" in li["class"]:
			link = li.find_all("p")[1].find("a").get('href') 
			getAnimesDescription(link, anime, True)


def parseHtmlAndGetEpisodes(html):
	__episodes__ = []
	soup = BeautifulSoup(html)
	for div in soup.find_all('div'):
		if "class" in div.attrs:
			if "mainBox" in div["class"]:
				__episodes__ = getEpisodes(div)
	return __episodes__


def getEpisodes(html):
	__episodes__ = []
	ul = html.find("ul")
	for li in ul.find_all("li"):
		if "class" in li.attrs:
			link = li.find_all("a")[1]
			__episode__ = {}
			__episode__["name"] = link.string.replace(" [Final]","")
			__episode__["url"] = link.get('href') 
			__episodes__.append(__episode__)
	return __episodes__