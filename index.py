import os
import traceback
import json
import requests

from flask import Flask, request

from messages import get_message, search_keyword

token = os.environ.get('ACCESS_TOKEN')

app = Flask(__name__)



def send_attachment(sender, type, payload):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "attachment": {
                "type": type,
                "payload": payload,
            }
        }
    }


def send_text(sender, text):
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text
        }
    }


def send_message(payload):
    
    print payload
    requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)



## Ravi Updates start

def send_hr_info(sender, **kwargs):
 
    	some_text = kwargs.pop('some_text', None)	
    	query = 'q={}'.format(some_text)
	print "before URL"
	print query

	url = 'http://ec2-34-253-183-190.eu-west-1.compute.amazonaws.com:5000//parse?'\
                '{}'.format(query)

    	print (url)
	r = requests.get(url)
   	response = r.json()
	print(response)
	
        intent = response['intent']
    	intent_text = str(intent['confidence'])
   	intent_float = float(intent_text)
	
	print "intent float" + intent_float
	
	if intent_float > 0.4:
	    hr_message="I am great"
	    message = send_text(sender, hr_message)
	    send_message(message)
		
	
	#hr_message="I am great too"
	#message = send_text(sender, hr_message)
        
        send_message(message)
        return None

## Ravi updates end




@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            sender = data['entry'][0]['messaging'][0]['sender']['id']
	    print "in POST data"
            print(data)

            if 'message' in data['entry'][0]['messaging'][0]:
                message = data['entry'][0]['messaging'][0]['message']
                text = message['text']
		print text
		
		_return = send_hr_info(sender, some_text=text)
		return 'Ok'



        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"

if __name__ == '__main__':
    app.run(debug=True)
