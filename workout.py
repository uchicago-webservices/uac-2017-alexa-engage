import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def exercise_data(exercise_no):
	import csv
	with open('exercises.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			if exercise_no == int(row['id']):
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
	next()
	msg = render_template('welcome')+introduce()
	return question(msg)

def next():
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1
	session.attributes['exercise'] = exercise_data(session.attributes['exercise_no'])

	if session.attributes['exercise_no'] > session.attributes['exercise_total']:
		return False
	return True

def introduce():
	exercise = session.attributes['exercise']

	msg = ' Exercise '+str(exercise['id'])+'. '+exercise['title']+' '+render_template('exercise_options')
	return msg
	
@ask.intent("ExerciseIntent")
def exercise(todo):
	if todo != 'ready' and todo != 'explain' and todo != 'skip':
		return question('I did not understand. '+' '+render_template('exercise_options'))

	exercise = session.attributes['exercise']

	if todo == 'ready':
		msg = ready()

		if (next() == False):
			msg = msg + ' You are done. Nice job!'
			return statement(msg).standard_card(
				title=exercise['title'],
				text=exercise['image'],
				small_image_url=exercise['image'],
				large_image_url=exercise['image'])

		msg = msg + introduce()
		return question(msg).standard_card(
			title=exercise['title'],
			text=exercise['image'],
			small_image_url=exercise['image'],
			large_image_url=exercise['image']).reprompt(render_template('exercise_options'))

	if todo == 'explain':
		msg = explain()
		
		msg = '<speak>'+msg+'</speak>'
		return question(msg).standard_card(
			title=exercise['title'],
			text=exercise['image'],
			small_image_url=exercise['image'],
			large_image_url=exercise['image']).reprompt(render_template('exercise_options'))

	if todo == 'skip':
		if (next() == False):
			return statement(' You are done. Nice job!')

		msg = introduce()
		return question(msg).reprompt(render_template('exercise_options'))

	return


def explain():
	exercise = session.attributes['exercise']

	msg = exercise['instructions']
	msg = msg+' '+render_template('exercise_options')

	return msg

def ready():
	exercise = session.attributes['exercise']

	# todo: add audio file here
	msg = ' 3. 2. 1. '

	return msg




@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping")


# @ask.session_ended
# def session_ended():
# 	log.debug('Session Ended')
# 	return '', 200


if __name__ == '__main__':

    app.run(debug=True)
