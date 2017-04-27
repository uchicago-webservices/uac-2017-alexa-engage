import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def exercise_data():
	import csv
	with open('exercises.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if session.attributes['exercise_no'] == int(row['id']):
				id = int(row['id'])
				title = row['title']
				instructions = row['instructions']
				image = row['image']
				return row
	return


@ask.launch
def launch():
	session.attributes['exercise_total'] = 2
	session.attributes['exercise_no'] = 0
	return introduce(render_template('welcome'))

def introduce(msg):
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] > session.attributes['exercise_total']:
		return statement(msg+' You are done. Nice job!')

	exercise = exercise_data()
	text = msg+' Exercise '+str(exercise['id'])+'. '+exercise['title']+' '+render_template('exercise_options')
	return question(text).standard_card(
			title=exercise['title'],
			text=exercise['image'],
			small_image_url=exercise['image'],
			large_image_url=exercise['image'])
	
@ask.intent("ExerciseIntent")
def exercise(todo):
	if todo != 'ready' and todo != 'explain' and todo != 'skip':
		return question('I did not understand. '+' '+render_template('exercise_options'))

	if todo == 'ready':
		return ready()

	if todo == 'explain':
		return explain()

	if todo == 'skip':
		return skip()

	return


def explain():
	exercise = exercise_data()

	msg = exercise['instructions']

	msg = msg+' '+render_template('exercise_options')

	return question(msg)

def ready():
	exercise = exercise_data()

	msg = ' 10. 9. 8. 7. 6. 5. 4. 3. 2. 1. '

	return introduce(msg)

def skip():
	return introduce('')



@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping")



if __name__ == '__main__':

    app.run(debug=True)
