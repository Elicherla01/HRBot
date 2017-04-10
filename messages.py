import random


chat_responses = {}

chat_responses['i_do_not_know'] = [
    'Unfortuantely, I did not understand. Can you please try again? At this time i can help with OJP.',
]

chat_responses['error'] = [
    'There was a problem fetching information... =(',
    'Something went wrong here ... sorry... :/',
]

chat_responses['no_answer'] = [
    'I did not understand anything... =(',
    'Sorry, I do not understand. )',
    'I did not take ... it was bad... ;(',
]



chat_responses['greetings'] = [
    'Hi, how are you? I can help you with OJP',
    'Hi! how is your day? I can help you with OJP',

]

chat_responses['thanks'] = [
    'No worries 8)',
    'I appreciate it. <3',
    'What is this? I am just doing my job. :)',
]

chat_responses['good-bye'] = [
    'Come back again anytime:D',
    'Bye bye 8)',
]

chat_responses['criteria'] = [
    'All colleagues are eligible to apply for roles posted in OJP. Manager endorsement is required to support application. Initially to manage the scale of engineering and infrastructure SDE I and SE I roles, we will be prioritising applications from PSE colleagues. Eventually it will be open to all colleagues.',
    
]


def get_message(response_type):
    """
    Return a random string message from a given type
    """
    if response_type in chat_responses:
        return random.choice(chat_responses[response_type])
    return random.choice(chat_responses['no_answer'])


chat_keywords = {}

chat_keywords['greetings'] = [
    'hi',
    'ok',
    'hello',
    'helloo',
    'OK',
    'hey',
    'hi',
    'good morning',
    'good day',
    'good night',
    'good',
   
    
]

chat_keywords['good-bye'] = [
    'bye',
    'See you later',
    'bye',
    'bye bye',
    'bye-bye',

]


chat_keywords['thanks'] = [
    'Thank you',
    'See you',
    'Thanks',
    'thank you',
    'thanks',
     'great',
     'fine',
]

chat_keywords['criteria'] = [
    'What is the criteria?',
    'Can you tell me criteria?',
    'Can you please tell me criteria?',
    'criteria please',
    'criteria',
    'What is the criteria',
    'Can you tell me criteria',
    'Can you please tell me criteria',
    'OJP',
    'ojp',
    
   ]

def search_keyword(raw_text):
    """
    Search for a keyword on a text and returns the right message
    """
    for key, word_list in chat_keywords.items():
        for word in word_list:
            if word in raw_text.lower():
                return get_message(key)
    return None
