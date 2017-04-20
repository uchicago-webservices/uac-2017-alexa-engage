# Simple workout #

Built with guidance from 

https://alexatutorial.com/flask-ask/
https://alexatutorial.com/2

It works with a unique skill name, e.g., 'engage workout'.

To run:

1. In first Terminal window:

	$ python workout.py

2. In second Terminal window:

	$ /Users/pezzutidyer/libraries/ngrok http 5000

3. Use Forwarding URL in your Amazon developer config for this skill, under the Configuration tab.

4. Go to http://echosim.io/ and test with 'Alexa start Engage Workout'.


# Deploy and Beta Test #

https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa

Add a tester of your skill with these instructions.

https://developer.amazon.com/blogs/post/Tx2EN8P2AHAHO6Y/How-to-Add-Beta-Testers-to-Your-Skills-Before-You-Publish