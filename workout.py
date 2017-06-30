import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
	start_session()

	msg = render_template('welcome')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))

def start_session():
	session.attributes['exercise_total'] = 3
	session.attributes['exercise_no'] = 0
	return	

def next():
	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	if session.attributes['exercise_no'] > session.attributes['exercise_total']:
		return False
	
	return True


def exercise_message():
	exercise_no = session.attributes['exercise_no']
	template_name = 'ex_'+`exercise_no`
	msg = ' '+render_template(template_name)
	return msg
	

@ask.intent("ReadyIntent")
def ready():
	exercise_no = session.attributes['exercise_no']
	msg = ''

	if (next() == False):
		msg = msg+' '+render_template('done')
		msg = '<speak>'+msg+'</speak>'
		return statement(msg)

	msg = msg+exercise_message()+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))


@ask.intent("GoDirectlyIntent")
def godirectly(exercise_no):
	start_session()

	session.attributes['exercise_no'] = int(exercise_no) - 1
	msg = ''

	if (next() == False):
		msg = msg+' '+render_template('done')
		msg = '<speak>'+msg+'</speak>'
		return statement(msg)

	msg = msg+exercise_message()+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))


@ask.intent("AMAZON.StopIntent")
def stop():
    return statement(render_template('stop'))

@ask.intent("AMAZON.HelpIntent")
def help():
	msg = render_template('help')+' '+render_template('continue_prompt')
	msg = '<speak>'+msg+'</speak>'
	return question(msg).reprompt(render_template('exercise_options'))

# @ask.session_ended
# def session_ended():
# 	log.debug('Session Ended')
# 	return '', 200


if __name__ == '__main__':

    app.run(debug=True)
