import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def launch():
    return question("Ready to exercise?")

@ask.intent("ReadyIntent")
def ready():
    return question("you are ready. how was it?")

@ask.intent("RatingIntent")
def rating(score):
    msg = 'you said it was {}'.format(score)
    return statement(msg)

@ask.intent("AMAZON.StopIntent")
def stop():
    return statement("Stopping")



if __name__ == '__main__':

    app.run(debug=True)
