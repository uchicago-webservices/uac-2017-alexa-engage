import logging, time

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


def load_routine(routine_name):
	if routine_name == '':
		session.attributes['routine'] = 'Monday'
		day_of_week = time.strftime("%A")	
		if (day_of_week in ['Tuesday','Thursday']):
			session.attributes['routine'] = 'Tuesday'
		if (day_of_week in ['Saturday','Sunday']):
			session.attributes['routine'] = 'Saturday'
	else:
		session.attributes['routine'] = routine_name

	return True

def load_exercise_data():
	routine = session.attributes['routine']

	import csv		
 	with open('exercises.csv') as csvfile:		
		reader = csv.DictReader(csvfile)
		for row in reader:		
			if row['routine'] == routine:
				session.attributes['exercises'].append(row)
	return


def photo_url_prefix():
	return 'https://s3.amazonaws.com/engage-alexa-exercise-photos/'


def exercise_reply_info():
	d = dict()
	exercise_no = session.attributes['exercise_no'] - 1
	d['template_name'] = session.attributes['exercises'][exercise_no]['template_name']
	d['title'] = str(session.attributes['exercise_no'])+'. '+session.attributes['exercises'][exercise_no]['exercise_name']
	d['content'] = session.attributes['exercises'][exercise_no]['card_text']

	if (session.attributes['exercises'][exercise_no]['photo']):
		d['image_url'] = photo_url_prefix()+session.attributes['exercises'][exercise_no]['photo']
	else:
		d['image_url'] = False

	return d


def exercise_question():
	reply = exercise_reply_info()

	msg = ' '+render_template(reply['template_name'])
	msg = '<speak>'+msg+'</speak>'

	if (reply['image_url'] == False):
		return question(msg).simple_card(
				title=reply['title'],
				content=reply['content']
				).reprompt(render_template('exercise_options'))	

	else:
		return question(msg).standard_card(
				title=reply['title'],
				text=reply['content'],
				small_image_url=reply['image_url'],
				large_image_url=reply['image_url']
				).reprompt(render_template('exercise_options'))	


def exercise_statement():
	reply = exercise_reply_info()

	msg = ' '+render_template(reply['template_name'])+' '+render_template('done')
	msg = '<speak>'+msg+'</speak>'

	card_content = reply['content']+ "\n\n You are done!"

	if (reply['image_url'] == False):
		return statement(msg).simple_card(
				title=reply['title'],
				content=card_content
				)

	else:
		return statement(msg).standard_card(
				title=reply['title'],
				text=card_content,
				small_image_url=reply['image_url'],
				large_image_url=reply['image_url']
				)


def misunderstand_question():
	msg = render_template('misunderstand')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).simple_card(
		title="EngAGE Exercise didn't understand", 
		content='"READY" or "OK" to go to the next exercise.\n"STOP" to quit at any time.\n"HELP" for instructions.'
		).reprompt(render_template('exercise_options'))


def wait_question():
	msg = render_template('wait')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).simple_card(
		title="Waiting...", 
		content='Say "Repeat" to go back to the exercises.'
		).reprompt(render_template('exercise_options'))


def start_session():
	if session.attributes.get('routine') is None:
		load_routine('')

	session.attributes['exercise_no'] = 0
	session.attributes['exercises'] = []
	load_exercise_data()
	session.attributes['exercise_total'] = len(session.attributes['exercises'])
	return	


def next():
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] >= session.attributes['exercise_total']:
		return False
	
	return True


@ask.launch
def launch():
	start_session()
	return ready('OK')


@ask.intent("ReadyIntent")
def ready(phrase):
	ready_phrases = ['ready','yes','go','next','OK','skip','resume', 'o.k.', 'okay', 'k', 'yeah', 'yeh']
	not_ready_phrases = ['wait','pause','not ready','no']
	repeat_phrases = ['repeat','again','go back']

	if (phrase in ready_phrases):
		if (next() == False):
			return exercise_statement()
		return exercise_question()

	if (phrase in repeat_phrases):
		return exercise_question()

	if (phrase in not_ready_phrases):
		return wait_question()

	return misunderstand_question()


@ask.intent("RoutineIntent")
def routine(routine_name):
	routines = ['Monday','Tuesday','Saturday']

	if (routine_name in routines):
		session.attributes['routine'] = routine_name
		start_session()
		next()
		return exercise_question()	

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
		return exercise_statement()

	return exercise_question()


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement(render_template('stop'))


@ask.intent("AMAZON.CancelIntent")
def cancel():
    return statement(render_template('stop'))


@ask.intent("AMAZON.HelpIntent")
def help():
	msg = render_template('help')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).simple_card(
		title='Help with EngAGE Exercise', 
		content='"READY" or "OK" to go to the next exercise.\n"REPEAT" to hear again.\nInterrupt with my wake word (e.g. Alexa or Echo).\n"WAIT" for extra time.\n"STOP" to quit at any time.'
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
