# -*- coding: utf-8 -*

import urllib.request as url
import urllib.parse as parse
from bs4 import BeautifulSoup

"""
    Parser that parse a wikipedia page and gets the first links of the page.
	Change the website page to change the language.
	
	Ex :
	
	import linksParser as p
	
	# Changing to french
	p.website = "https://fr.wikipedia.org/wiki/"
	# Gets all the links in the 2 first sentences of the 3 first paragraphs
	getLinks("pomme", 3, 2)
	
	# And it returns
	# (False, ['Fruit (alimentation humaine)', 'Alimentation', 'Pépin (graine)', 'Goût',
	# 'Sucre', 'Acide', 'Astringence', 'Botanique', 'Fruit complexe', 'Pommier domestique', 
	# 'Espèce', 'Malus domestica', 'Variété (botanique)', 'Cultivars', 'Fruit défendu', 
	# 'Livre de la Genèse', 'Occident', 'P<<<éché originel', 'Acte sexuel'])	
"""

__authors__ = "Rémi Monthiller @LeDernier"
__version__ = "1.0"
__email__ = "remi.monthiller@etu.enseeiht.fr"
__status__ = "finished"

website = "https://en.wikipedia.org/wiki/"	   

def isValid(ref,paragraph):
	if not ref or "#" in ref or "//" in ref or ":" in ref:
		return False
	if "/wiki/" not in ref:
		return False
	if ref not in paragraph:
		return False
	# Just check if it is not inside parenthesis.
	prefix = paragraph.split(ref,1)[0]
	if prefix.count("(")!=prefix.count(")"):
		return False
	return True

def validTag(tag):
	if("class" in tag.attrs):
		return False
	name = tag.name
	isParagraph = name == "p"
	isList = name == "ul"
	return isParagraph or isList

def getLinks(word, pNb=-1, sNb=-1):
	# Init
	word = word.capitalize()
	links = []
	
	try:
		# Parsing
		req = url.Request(website + parse.quote(word), headers={'User-Agent' : "Magic Browser"})
		page = url.urlopen(req)
		data = page.read()
		soup = BeautifulSoup(data, 'html.parser')
		homonymie = bool(soup.find(id="homonymie"))
		if(homonymie):
			# print(homonymie.text)
			pNb = -1
			sNb = -1
		soup = soup.find(id="mw-content-text")
		soup = soup.find(class_="mw-parser-output")
		
		paragraphs = soup.find_all(validTag, recursive=False)
		
		if(pNb < 0):
			pNb = len(paragraphs)
		i = 0
		while (i < len(paragraphs) and i < pNb):
			paragraph = paragraphs[i]
			str_p = str(paragraphs[i])
			sentences = str_p.split('.')
			if(sNb < 0):
				sNb = len(sentences)
			j = 0
			while(j < len(sentences) and j < sNb):
				sentence = BeautifulSoup(sentences[j], 'html.parser')
				for link in sentence.find_all("a"):
					ref = link.get("href")
					if isValid(str(ref),str(paragraph)):
						title = link.get("title")
						if((not homonymie) or title.startswith(word)):
							links.append(title)
				j += 1
			i += 1
			# If no link found, just check next paragraph	
			if(not links):
				pNb += 1
		return homonymie, links
	except:
		return "error", "error"