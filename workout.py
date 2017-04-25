import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
	session.attributes['exercise_total'] = 2
	session.attributes['exercise_no'] = 1
	msg = render_template('welcome') + introduce()
	return question(msg)

def introduce():
	template = 'exercise_'+str(session.attributes['exercise_no'])+'_title'
	text = render_template(template);
	text = ' ' + text + ' Say Ready, Explain or Skip. '
	return text;

@ask.intent("ExerciseOneIntent")
def exercise_one(todo):
	msg = ""

	if todo == 'ready':
		msg = '1. 2. 3. 4. 5. 6. 7. 8. 9. 10. '

	if todo == 'explain':
		template = 'exercise_'+str(session.attributes['exercise_no'])+'_instructions'
		msg = render_template(template);

	if session.attributes['exercise_no'] == session.attributes['exercise_total']:
		msg = msg + ' You are done. Nice job!'
		return statement(msg)

	session.attributes['exercise_no'] = session.attributes['exercise_no'] + 1

	msg = msg + introduce()

	return question(msg)

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping")



if __name__ == '__main__':

    app.run(debug=True)
