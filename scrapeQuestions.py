import requests
import bs4
import json
import os
from unidecode import unidecode
# Fixes the text parsing problem from the museumhack website

FAKE_HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
QUESTIONS = []

def update_file(jsonFile):
	if os.path.exists(jsonFile) == False:
		currentQuestions = {"questions": []}
	else:
		currentQuestions = json.load(open(jsonFile))

	currentQuestions['questions'] = set(currentQuestions['data'])
	# This is a hacky way of making dup lookup constant time...

	for val in QUESTIONS:
		if val not in currentQuestions['data']:
			currentQuestions['data'].add(val)

	currentQuestions['questions'] = list(currentQuestions['data'])
	# make it a list again...

	with open(jsonFile, 'w') as fp:
		# overwrite file
		json.dump(currentQuestions, fp, indent=4)

def get_site(url):
	res = requests.get(url, headers=FAKE_HEADERS)
	return res.text

def get_bs4(url):
	return bs4.BeautifulSoup(get_site(url), 'lxml')


if __name__ == '__main__':
	a = get_bs4("https://museumhack.com/list-icebreakers-questions/")
	for val in a.select(".text-h-2 ol li"):
		question = unidecode(val.getText())
		QUESTIONS.append(question)

	update_file("file.json")