# -*- coding: utf-8 -*-
""" simple fact sample app """

from __future__ import print_function

import random
import time


SKILL_NAME = "La Papa Caliente"
GET_INIT_MESSAGE = "Bienvenido a la papa caliente, quieres comenzar a jugar? "
HELP_MESSAGE = "Juega la papa caliente con Alexa, ella te dirá cuando la papa se quemó, quieres empezar a jugar?"
HELP_REPROMPT = "  Quieres seguir jugando?"
STOP_MESSAGE = "Sigue divirtiéndote!, adiós!" 
FALLBACK_MESSAGE = "No te entendí bien.  Quieres jugar?"
FALLBACK_REPROMPT = "Quieres jugar?"
LA_PAPA ="<audio src='https://s3.amazonaws.com/papa-caliente/ring.mp3'/>"+"La papa caliente "
SE_QUEMA = " Se quema, "+"<break time='0.3s'/>"
SE_QUEMO= "<break time='0.3s'/>"+ "se quemó!"+ "<audio src='https://s3.amazonaws.com/papa-caliente/bomb.mp3'/>"


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
    if intent_name == "comenzar":
        return get_fact_response()
    elif intent_name == "otravez":
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
    speechOutput = GET_INIT_MESSAGE 

    return response(speech_response_ssml(speechOutput, False))

def get_fact_response():
    """ get and return a random fact """
    randomi = random.randint(1, 7)
    count=0
    sequema= SE_QUEMA
    for x in range(1, randomi):
        sequema += SE_QUEMA
        if (x%2)==0:
            sequema += "<audio src='https://s3.amazonaws.com/papa-caliente/tictoc.mp3'/>"
    speechOutput = LA_PAPA + sequema + SE_QUEMO + "<break time='1.3s'/>"+ HELP_REPROMPT

    return response(speech_response_ssml(speechOutput, False))

def get_help_response():
    """ get and return the help string  """

    speech_message = HELP_MESSAGE
    return response(speech_response_prompt(speech_message,
                                                       speech_message, False))
def get_launch_response():
    """ get and return the help string  """
    
    return get_init_response()

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
