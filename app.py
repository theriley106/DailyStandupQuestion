from flask import Flask, render_template, request, url_for, redirect, Markup, jsonify, make_response, send_from_directory, session
import json
import random

app = Flask(__name__, static_url_path='/static')
QUESTION_FILE = "questions.json"

QUESTIONS = json.load(open(QUESTION_FILE))["questions"]


@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/new', methods=['GET'])
def newQuestion():
	return jsonify({"question": random.choice(QUESTIONS)})

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000)