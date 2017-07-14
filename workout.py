import logging, time

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def load_exercise_data():
	routine = 'Monday'
	day_of_week = time.strftime("%A")	
	if (day_of_week in ['Tuesday','Thursday','Saturday']):
		routine = 'Tuesday'

	import csv		
 	with open('exercises.csv') as csvfile:		
		reader = csv.DictReader(csvfile)
		for row in reader:		
			if row['routine'] == routine:
				session.attributes['exercises'].append(row)
	return


def photo_url_prefix():
	return 'https://s3.amazonaws.com/engage-alexa-exercise-photos/'


def exercise_question():
	exercise_no = session.attributes['exercise_no'] - 1
	template_name = session.attributes['exercises'][exercise_no]['template_name']
	exercise_title = session.attributes['exercises'][exercise_no]['exercise_name']
	photo_url = photo_url_prefix()+session.attributes['exercises'][exercise_no]['photo']
	card_text = session.attributes['exercises'][exercise_no]['card_text']

	msg = ' '+render_template(template_name)
	msg = msg+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'

	if (photo_url):
		return question(msg).standard_card(
				title=exercise_title,
				text=card_text,
				small_image_url=photo_url,
				large_image_url=photo_url
				).reprompt(render_template('exercise_options'))	

	else:
		return question(msg).reprompt(render_template('exercise_options'))	


def misunderstand_question():
	msg = render_template('misunderstand')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).simple_card(
		title="EngAGE Exercise didn't understand", 
		content='"READY" or "OK" to go to the next exercise.\n"STOP" to quit at any time.\n"HELP" for instructions.'
		).reprompt(render_template('exercise_options'))


def wait_question():
	msg = render_template('wait')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).simple_card(
		title="Waiting...", 
		content='Say "OK" to continue.'
		).reprompt(render_template('exercise_options'))


def start_session():
	session.attributes['exercise_no'] = 0
	session.attributes['exercises'] = []
	load_exercise_data()
	session.attributes['exercise_total'] = len(session.attributes['exercises'])
	return	


def next():
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] > session.attributes['exercise_total']:
		return False
	
	return True


@ask.launch
def launch():
	start_session()
	return ready('OK')


@ask.intent("ReadyIntent")
def ready(phrase):
	ready_phrases = ['ready','yes','go','next','OK','skip','resume']
	not_ready_phrases = ['wait','pause','not ready','no']

	if (phrase in ready_phrases):
		exercise_no = session.attributes['exercise_no']
		msg = ''

		if (next() == False):
			photo_url = photo_url_prefix()+'finding_activities_you_enjoy.png'
			msg = msg+' '+render_template('done')
			msg = '<speak>'+msg+'</speak>'
			return statement(msg).standard_card(
					title="You are done!",
					text="Lets exercise again soon!",
					small_image_url=photo_url,
					large_image_url=photo_url
					)

		return exercise_question()

	if (phrase in not_ready_phrases):
		return wait_question()

	return misunderstand_question()


@ask.intent("GoDirectlyIntent")
def godirectly(exercise_no):
	start_session()

	if (exercise_no is None):
		return misunderstand_question()

	if (exercise_no.isdigit() == False):
		return misunderstand_question()

	if (int(exercise_no) < 1 or int(exercise_no) > session.attributes['exercise_total']):
		return misunderstand_question()

	session.attributes['exercise_no'] = int(exercise_no) - 1
	msg = ''

	if (next() == False):
		msg = msg+' '+render_template('done')
		msg = '<speak>'+msg+'</speak>'
		return statement(msg)

	return exercise_question()


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement(render_template('stop'))


@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement(render_template('stop'))


@ask.intent("AMAZON.HelpIntent")
def help():
	msg = render_template('help')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).simple_card(
		title='Help with EngAGE Exercise', 
		content='"READY" or "OK" to go to the next exercise.\n"WAIT" for extra time.\n"STOP" to quit at any time.'
		).reprompt(render_template('exercise_options'))




# @ask.session_ended
# def session_ended():
# 	log.debug('Session Ended')
# 	return '', 200


if __name__ == '__main__':
	# We don't want to keep the line below forever.
	# Waiting on resolution to https://github.com/johnwheeler/flask-ask/issues/152.
    # app.config['ASK_VERIFY_REQUESTS'] = False 
    app.run(debug=True)
