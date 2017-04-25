import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

# there is a problem here: i can't get the first row!
# save to session?
def exercise_data():
	import csv
	with open('exercises.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if session.attributes['exercise_no'] == row['id']:
				id = row['id']
				title = row['title']
				instructions = row['instructions']
				image = row['image']
				break
	return row

@ask.launch
def launch():
	session.attributes['exercise_total'] = 2
	session.attributes['exercise_no'] = 1
	msg = render_template('welcome') + introduce()
	return question(msg)

def introduce():
	exercise = exercise_data()
	text = ' Exercise '+str(exercise['id'])+'. '+exercise['title']+' ' +render_template('exercise_options')
	return text;

@ask.intent("ExplainIntent")
def explain(todo):
	exercise = exercise_data()

	msg = exercise['instructions']

	msg = msg + render_template('exercise_options')

	return question(msg)

@ask.intent("ReadyIntent")
def ready(todo):
	exercise = exercise_data()

	msg = '1. 2. 3. 4. 5. 6. 7. 8. 9. 10. '

	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] >= session.attributes['exercise_total']:
		return statement('You are done. Nice job!')

	msg = msg + introduce()

	return question(msg)

@ask.intent("SkipIntent")
def skip(todo):
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] >= session.attributes['exercise_total']:
		return statement('You are done. Nice job!')

	msg = introduce()

	return question(msg)

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping")



if __name__ == '__main__':

    app.run(debug=True)
