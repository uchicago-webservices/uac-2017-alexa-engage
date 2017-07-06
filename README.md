# Local Development #

The dev skill is intended for development only. It uses ngrok to allow the programmer to run the skill program from a laptop temporarily. It's built with guidance from https://alexatutorial.com/flask-ask/ and https://alexatutorial.com/2.


To run:

1. In first Terminal window:

	$ python workout.py

2. In second Terminal window:

	$ /Users/pezzutidyer/libraries/ngrok http 5000

3. Log in at https://developer.amazon.com. Go to the Alexa section, Alexa Skills set, Engage DEV skill, Configuration tab. For Service Endpoint Type, choose HTTPS and North America, and paste in the Forwarding URL from ngrok.

4. Go to http://echosim.io/ and test with the phrase 'Alexa start engage dev' or 'start engage dev'.

If you change data or templates, you will need to stop and restart the python script. You do not need to restart ngrok.


## Issues and To-dos ##

### Instructions are too fast. ###
You can add pauses with SSML text. See https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/speech-synthesis-markup-language-ssml-reference.

How long will each exercise take to complete?

### Use cards for photos. ###
This was deemed not very useful by the EngAGE team; maybe revisit if using Echo Show. See https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/providing-home-cards-for-the-amazon-alexa-app#common-issues-when-including-images-in-standard-cards.
1. Host on S3.
2. Make images public.
3. Set up CORS. See http://docs.aws.amazon.com/AmazonS3/latest/user-guide/add-cors-configuration.html.

### Reprompt user if he/she doesn't reply. ###
Can't test this with echosim. See https://forums.developer.amazon.com/questions/44478/how-do-i-test-reprompt-message-with-simulator.html.

### Add audio for exercise countdown. ###
Convert pm3 files. See https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/speech-synthesis-markup-language-ssml-reference#h3_converting_mp3.

	$ ffmpeg -i <input-file> -ac 2 -codec:a libmp3lame -b:a 48k -ar 16000 <output-file.mp3>

You might get this error, but it will still work.

	[mp3 @ 0x7ff4dc803a00] Header missing
	Error while decoding stream #0:0: Invalid data found when processing input


### Save a session so user can pick up on next exercise. ###



# Beta Deployment and Testing #

We'll use the beta deployment for client review and testing.

For the first time, set up dependencies for Zappa, AWS CLI, etc. See https://developer.amazon.com/blogs/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa.

Zappa deploy and update use your AWS credentials in ~/.aws. Rose has a copy of the credential files. You can set up a new AWS account with the following.

	$ aws configure --profile myprofilename

Then deploy from your project's directory. Here are instructions for the very first deployment.

	$ virtualenv venv
	$ source venv/bin/activate
	(venv) $ pip install flask-ask zappa requests awscli
	(venv) $ pip install -U botocore
	(venv) $ aws configure
	(venv) $ zappa init
	(venv) $ zappa deploy beta

To update, you don't need to do most of the set-up steps. Just do these from the project root:

	$ virtualenv venv
	$ source venv/bin/activate
	$ zappa update beta

Make note of the URL in the output. It looks something like https://625ff9gf9k.execute-api.us-east-1.amazonaws.com/beta.

Log in at https://developer.amazon.com. Go to the Alexa section, Alexa Skills. Set up a new skill, Engage BETA. For Service Endpoint Type, choose HTTPS and North America, and paste in the Zappa URL.

Test in test the Alexa skill Test tab. The invocation phrase should be 'Alexa start engage beta'.

## ImportError ##

If you have trouble deploying again (maybe you get an ImportError), trying using venv.zip instead of the venv directory you created with the above instructions.

## Cryptography warning during Zappa deployment ##
You may see this warning during a zappa deploy or update.

	$ zappa update prod
	Downloading and installing dependencies..
	 - cryptography==1.9: Warning! Using precompiled lambda package version 1.8.1 instead!

You will need to run this first to get cryptography in the right version.

	$ pip install cryptography==1.8.1


## Add a tester of your skill with these instructions. ##

https://developer.amazon.com/blogs/post/Tx2EN8P2AHAHO6Y/How-to-Add-Beta-Testers-to-Your-Skills-Before-You-Publish

## Troubleshooting ##

To view debugging in your Lambda function:

	$ virtualenv venv
	$ source venv/bin/activate
	$ zappa tail beta




# Prod Deployment #

The prod deployment is for the final skill that is certified by Amazon.

## Set up prod account and environment ##

Log in at awslogin.uchicago.edu with your CNet; choose "Account: uchicago-its-dev (384930876859)" and click the "admins" radio. 

I have already set up a zappa service user "EnageAlexaZappaDeveloper".

## Deployment ##

	$ virtualenv venv
	$ source venv/bin/activate
	$ zappa update prod

To make changes in the future:

	$ virtualenv venv
	$ source venv/bin/activate
	$ zappa update prod

## Certification ##

I deployed a prod version of this skill on 6/29/2017 in order to test the Amazon submission and review process. While under review, code changes cannot be made. The skill will have to be withdrawn first.

See https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/alexa-skills-kit-submission-checklist for certification guidelines.



# References #

Flask Ask: http://flask-ask.readthedocs.io/en/latest/

SSML: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/speech-synthesis-markup-language-ssml-reference

Gitter: https://gitter.im/johnwheeler/flask-ask/