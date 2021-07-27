from data_handler import add_increment_userDB, feed_catdb, check_catsdb, make_Catdb, check_onecatdb, check_lastDateTime, get_paidDB, set_paidDB, remove_Catdb
import json, re
import datetime
SKILLNAME = 'Hungry Cat'

spB = "<speak>"
spE = "</speak>"
def build_speechlet_response(title, output, reprompt_text, should_end_session, directives=[]):
    content = output.replace("\\n","").replace(".\n", ".")
    content = re.sub('<.*?>','',content, flags=re.DOTALL)
    
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'SSML',
                'ssml': reprompt_text
            }
        },
        'shouldEndSession': should_end_session,
        'directives': directives
        
    }
    
    

def build_response(session_attributes, speechlet_response): #, directives = {}
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }
    #,'directives': [directives]


def getCatName(session, intent_request):
    intent = intent_request['intent']
    catName = intent['slots']['getthecatname']['value'].lower()
    
    success = make_Catdb(session, catName)
    
    if success == 0:
        speech_output = "You aleady have a cat named %s" %(catName)
        card_title = "Duplicate cat name"
    else:
        speech_output = "%s is a nice name! <break/> You can now ask me to feed %s" %(catName, catName)
        card_title = "All ready to feed your cat!"

    
    should_end_session = True
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    
def whenFedIntent(session, intent_request):
    
    intent = intent_request['intent']
    add_increment_userDB(session)
    catName = intent['slots']['catname']['value'].lower()
    currentDate = datetime.datetime.now()


    if check_onecatdb(session, catName) == 0:
        speech_output = """Hello. <break/>. You either haven't added this cat, or have never fed them. Please say: feed the cat."""
        card_title = "You need to feed your cat first :)"
        should_end_session = False
    else:
        should_end_session = True
        try: 
            lastdatetime = check_lastDateTime(session, catName)
            timediff = str(currentDate - lastdatetime)
            timediff = timediff.split(",")
            #if there is a "-1 days, 08:00:00"
            if len(timediff) > 1:
                days = timediff[0].replace("-", "") + " "
                timesplit = timediff[1].split(":")
            else:
                days = ""
                timesplit = timediff[0].split(":")
            hours = timesplit[0]
            minutes = timesplit[1]
            #if hours is zero
            if int(hours) == 0:
                hours = ""
            else:
                if hours[0] == '0':
                    hours = hours.replace('0','')
                if hours == '1':
                    hours = str(hours) + " hour "
                else:
                    hours = str(hours) + " hours "
            #if minutes is zero
            if int(minutes) == 0:
                minutes = ""
            else:
                if minutes[0] == '0':
                    minutes = minutes.replace('0','')    
                minutes = "and " + str(minutes) + " minutes"
            
            
            timesentence = days + hours + minutes
            if timesentence == "":
                timesentence = "moments"
                
            speech_output = """%s was last fed %s ago.""" %(catName, timesentence)
            card_title =timesentence
        except Exception as e:
            print(e)
            speech_output = """%s has never been fed""" %(catName)
            card_title = "Never been fed"
    
    
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
   
    
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    
    
    print(lastdatetime)
    
    
def removeCatIntent(session, intent_request):
    intent = intent_request['intent']
    catName = intent['slots']['catname']['value'].lower()
    
    remove_Catdb(session, catName)
    
    speech_output = "%s was successfully removed."%(catName)
    should_end_session = True
    card_title = "Removed %s!" %(catName)
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    
        
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    
    
    
def feedTheCatIntent(session, intent_request):
    intent = intent_request['intent']
    add_increment_userDB(session)
    catName = intent['slots']['catname']['value'].lower()
    currentDate = datetime.datetime.now()
    
    #set_paidDB(session, 1)
    #check the first catname in the list
    #check_catsdb returns a dictionary
    
    # print(get_paidDB(session))
    # print(len(check_catsdb(session)))
    # print(check_catsdb(session)[0]['CatName'])
    
    if get_paidDB(session) == 0 and len(check_catsdb(session)) != 0:
        if check_catsdb(session)[0]['CatName'] != catName:
            #unpaid, different cat
            speech_output = "I see you want to record that %s is fed, but you're already keeping track of %s. <break/> If you'd like to remove %s <break/> please say remove cat. <break/> Otherwise <break/> Please consider supporting the premium version of this skill which supports multiple cats. To learn more, <break/> please say learn more about unlimited cats."%(catName.capitalize(), check_catsdb(session)[0]['CatName'].capitalize(),check_catsdb(session)[0]['CatName'].capitalize() )
            
            should_end_session = False
            card_title = "Learn about about unlimited cats!"
            speech_output = spB + speech_output + spE
            reprompt_text = speech_output
        
        else:
        #unpaid, same cat
            if len(check_onecatdb(session, catName)) == 0:
                make_Catdb(session, catName)
                
            feed_catdb(session, catName)
        
            speech_output = "%s is fed, and I've recorded the current time."%(catName.capitalize())
            should_end_session = True
            card_title = "Fed the cat!"
            speech_output = spB + speech_output + spE
            reprompt_text = speech_output
        
    else:
        #paid
        #everything passes, let them add or update the cat
    
        if len(check_onecatdb(session, catName)) == 0:
            make_Catdb(session, catName)
            
        feed_catdb(session, catName)
    
    
    #feed_catdb(session, catName)
    
        speech_output = "%s is fed, and I've recorded the current time."%(catName)
        should_end_session = True
        card_title = "Fed the cat!"
        speech_output = spB + speech_output + spE
        reprompt_text = speech_output
    
        
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
    

# --------------- Events ------------------

def get_help_response():
    session_attributes = {}
    card_title = "Welcome"
    speech_output = """I can keep track of when your cat was last fed. Ask me to feed your cat by saying to Alexa: <break/> Alexa <break/> Ask %s to feed the cat. \
    Ask for when your cat was last fed by saying <break/> Alexa <break/> ask %s when was the cat fed? <break/> Alternatively, <break/> just open the skill directly."""%(SKILLNAME, SKILLNAME)
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def get_welcome_response(session):
    
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    session_attributes = {}
    card_title = "Welcome"
    
    
    

    if len(check_catsdb(session)) == 0:
        speech_output = """Hello. <break/>. This skill will help you keep track of when you feed the cat. <break/> Simply say: Alexa - ask %s to feed the cat.""" %(SKILLNAME)
    else:
        speech_output = """Please tell me to feed the cat <break/> or ask <break/> When was the cat fed?"""
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def on_session_started(session_started_request, session):
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])
def on_launch(event, launch_request, session):
    add_increment_userDB(session)
    #userInstanceDB(session)
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response(session)
    
    
    
###################################################################
###########################PURCHASE FLOW###########################
def afterPurchase(session):
    set_paidDB(session, 1)
    card_title = "Thank you."
    speech_output = "Thank you for your purchase. We hope to help you keep track of all your hungry cats!"
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    should_end_session = False
        
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

   
def afterNotPurchase():
    card_title = "Not purchased."
    speech_output = "Nothing was purchased."
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    should_end_session = True
        
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
       
def afterRefund(session):
    #set_paidDB(session, 0)
    card_title = "Refund information sent."
    speech_output = "Refund information sent."
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    should_end_session = True
        
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))  
        
        
def refundIntent(session):
    #set_paidDB(session, 1)
    sessionAttributes = {}
    userID = session['user']['userId']
    speech_output  = spB + "Refunding Unlimited cats." + spE
    reprompt_text = spB + "Refunding Unlimited cats." + spE
    card_title = "Refunding."
    should_end_session = True
    
    message = {}
    directive = [{
					'type': "Connections.SendRequest",
            'name': "Cancel",
            'payload': {
                'InSkillProduct': {
                    'productId': "amzn1.adg.product.f4516fc5-ce5f-444e-a4a8-b3ea51a66351",
                }
            
            },
            'token': userID
				}
				]
    sessionAttributes = {}
    return build_response(sessionAttributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session, directive))

def purchaseIntent(session):
    #set_paidDB(session, 1)
    sessionAttributes = {}
    userID = session['user']['userId']
    speech_output  = spB + "Purchasing Unlimited Cats." + spE
    reprompt_text = spB + "Purchasing Unlimited Cats." + spE
    card_title = "Purchasing."
    should_end_session = True
    
    
    directive = [{
					'type': "Connections.SendRequest",
            'name': "Buy",
            'payload': {
                'InSkillProduct': {
                    'productId': "amzn1.adg.product.f4516fc5-ce5f-444e-a4a8-b3ea51a66351",
                }
            
            },
            'token': userID
				}
				]
    sessionAttributes = {}
    return build_response(sessionAttributes, build_speechlet_response(card_title,speech_output,reprompt_text,should_end_session, directive))
        
def WhatCanIBuyIntent():
    card_title = "What Can I Buy?"
    speech_output = "This skill offers a paid feature that keeps track of every cat's feeding time! You'll be able to add an unlimited number of cats."
    speech_output = spB + speech_output + spE
    reprompt_text = speech_output
    should_end_session = False
        
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))        
        
def WhatDidIBuyIntent(session):
    card_title = "What Did I Buy?"
    if get_paidDB(session) == 1:
        speech_output = "Congrats! You purchased a paid feature that offers keeping track of all of your cats feeding times. "
        speech_output = spB + speech_output + spE
        reprompt_text = speech_output
        
    else:
        speech_output = "You haven't purchased anything! <break/> However, this skill offers a paid feature that lets you keep track of more than one cat's feeding time. <break/> To learn more, say: <break/> learn more about unlimited cats. "
        speech_output = spB + speech_output + spE
        reprompt_text = speech_output
    should_end_session = False
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
########################################################
########################################################    
    
    
##############################################
#############################################
    
def on_intent(intent_request, session):
    #userInstanceDB(session)
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    if intent_name == "FeedTheCatIntent":
        return feedTheCatIntent(session, intent_request)
    elif intent_name == "WhenFedIntent":
        return whenFedIntent(session, intent_request)
    elif intent_name == "RemoveCatIntent":
        return removeCatIntent(session, intent_request)
    elif intent_name == "PurchaseIntent":
        return purchaseIntent(session)
    elif intent_name == "WhatDidIBuyIntent":
        return whatDidIBuyIntent(session)
    elif intent_name == "WhatCanIBuyIntent":
        return whatCanIBuyIntent(session)
    elif intent_name == "RefundIntent":
        return RefundIntent(session)
    elif intent_name == "AMAZON.HelpIntent":
         return get_help_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
         return handle_session_end_request()
    else:
         return handle_session_end_request()
    #     #raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for using %s. " \
                    "Have a nice day! "%(SKILLNAME)
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    speech_output  = spB + speech_output + spE
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        


# --------------- Main handler ------------------
def lambda_handler(event, context):
    session = event['session']

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event, event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
    elif event['request']['type'] == "Connections.Response":
        if event['request']['name'] == "Buy":
            if event['request']['payload']['purchaseResult'] == "ACCEPTED":
                return afterPurchase(session)
            else:
                return afterNotPurchase()
        else:
            return afterRefund(session)
    else:
        return handle_session_end_request()        
