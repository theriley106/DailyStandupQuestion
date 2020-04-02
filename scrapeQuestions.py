import requests
import bs4
import json
import os
import re
from unidecode import unidecode
# Fixes the text parsing problem from the museumhack website

FAKE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
QUESTIONS = []

def update_file(jsonFile):
	if os.path.exists(jsonFile) == False:
		currentQuestions = {"questions": []}
	else:
		currentQuestions = json.load(open(jsonFile))

	currentQuestions['questions'] = set(currentQuestions['questions'])
	# This is a hacky way of making dup lookup constant time...

	for val in QUESTIONS:
		if val not in currentQuestions['questions']:
			currentQuestions['questions'].add(val)

	currentQuestions['questions'] = list(currentQuestions['questions'])
	# make it a list again...

	with open(jsonFile, 'w') as fp:
		# overwrite file
		json.dump(currentQuestions, fp, indent=4)

def get_site(url):
	res = requests.get(url, headers=FAKE_HEADERS)
	return res.text

def get_bs4(url):
	return bs4.BeautifulSoup(get_site(url), 'lxml')

def startersWorld(url):
	questions = []
	page = get_bs4(url)
	for val in page.select("#genesis-content p"):
		text = val.getText()
		if re.match("\d+\.\s+", text):
			questions.append(unidecode(text.partition(" ")[2]))
	return questions

def defaultScraper(url, cssSelector):
	return [unidecode(val.getText()) for val in get_bs4(url).select(cssSelector)]

# This is a key value pair of url and custom function to parse them
CUSTOM_SCRAPING_METHOD = {
	"https://conversationstartersworld.com/icebreaker-questions/": startersWorld,
}


# This is a key value pair of the url and CSS selector to parse them
URL_CSS_SELECTOR_MAP = {
	"https://museumhack.com/list-icebreakers-questions/": ".text-h-2 ol li",
	"https://improb.com/icebreaker-questions-adults/": "li strong",
}


if __name__ == '__main__':
	for url, function in CUSTOM_SCRAPING_METHOD.iteritems():
		for question in function(url):
			QUESTIONS.append(question)

	for url, selector in URL_CSS_SELECTOR_MAP.iteritems():
		for question in defaultScraper(url, selector):
			QUESTIONS.append(question)

	update_file("file.json")