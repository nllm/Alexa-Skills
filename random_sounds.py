# -*- coding: utf-8 -*-
""" simple fact sample app """

from __future__ import print_function

import random
import time


data = [ "https://s3.amazonaws.com/aladrar/c1.mp3", "https://s3.amazonaws.com/aladrar/c2.mp3","https://s3.amazonaws.com/aladrar/c3.mp3",
"https://s3.amazonaws.com/aladrar/c4.mp3","https://s3.amazonaws.com/aladrar/c5.mp3","https://s3.amazonaws.com/aladrar/c6.mp3",
"https://s3.amazonaws.com/aladrar/m1.mp3","https://s3.amazonaws.com/aladrar/m2.mp3","https://s3.amazonaws.com/aladrar/m3.mp3",
"https://s3.amazonaws.com/aladrar/g1.mp3","https://s3.amazonaws.com/aladrar/g2.mp3","https://s3.amazonaws.com/aladrar/g3.mp3"
]


SKILL_NAME = "A Ladrar"
INIT="<audio src='"
FIN="'/>"
HELP_MESSAGE = "Esta skill me permite ladrar, hay diferentes tipos de ladridos, quieres que ladre?"
HELP_REPROMPT = "Quieres que siga ladrando?"
STOP_MESSAGE = "Adiós!"
FALLBACK_MESSAGE = "Lo siento, solo puedo ladrar"
FALLBACK_REPROMPT = "Quieres que ladre?"


# --------------- App entry point -----------------

def lambda_handler(event, context):
    """  App entry point  """

    #print(event)

    if event['session']['new']:
        on_session_started()

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended()

# --------------- Response handlers -----------------

def on_intent(request, session):
    """ called on receipt of an Intent  """

    intent_name = request['intent']['name']

    # process the intents
    if intent_name == "ladrar":
        return get_fact_response()
    elif intent_name == "AMAZON.YesIntent":
        return get_fact_response()
    elif intent_name == "AMAZON.NoIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.HelpIntent":
        return get_help_response()
    elif intent_name == "AMAZON.StopIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.CancelIntent":
        return get_stop_response()
    elif intent_name == "AMAZON.FallbackIntent":
        return get_fallback_response()
    else:
        print("invalid Intent reply with help")
        return get_help_response()

def get_init_response():
    """ get and return a random fact """
    speechOutput = "HOLA" 

    return response(speech_response_ssml(speechOutput, False))

def get_fact_response():
    """ get and return a random fact """
    randomFact = random.choice(data)
    cardcontent = randomFact
    speechOutput =  INIT+randomFact+FIN+HELP_REPROMPT

    return response(speech_response_ssml(speechOutput, False))

def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
def get_launch_response():
    """ get and return the help string  """
    
    return get_fact_response()

def get_stop_response():
    """ end the session, user wants to quit the game """

    speech_output = STOP_MESSAGE
    return response(speech_response(speech_output, True))

def get_fallback_response():
    """ end the session, user wants to quit the game """

    speech_output = FALLBACK_MESSAGE
    return response(speech_response(speech_output, False))

def on_session_started():
    """" called when the session starts  """
    #print("on_session_started")

def on_session_ended():
    """ called on session ends """
    #print("on_session_ended")

def on_launch(request):
    """ called on Launch, we reply with a launch message  """

    return get_launch_response()


# --------------- Speech response handlers -----------------

def speech_response(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

def speech_response_ssml(output, endsession):
    """  create a simple json response  """
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>" 
        },
        'shouldEndSession': endsession
    }


def response_ssml_text_and_prompt(output, endsession, reprompt_text):
    """ create a Ssml response with prompt  """

    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" +output +"</speak>" 
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': "<speak>" +reprompt_text +"</speak>"
            }
        },
        'shouldEndSession': endsession
    }

def speech_response_prompt(output, reprompt_text, endsession):
    """ create a simple json response with a prompt """

    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': endsession
    }

def response(speech_message):
    """ create a simple json response  """
    return {
        'version': '1.0',
        'response': speech_message
    }
