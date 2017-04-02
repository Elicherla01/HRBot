import os
import traceback
import json
import requests

from flask import Flask, request

from messages import get_message, search_keyword

token = os.environ.get('ACCESS_TOKEN')

app = Flask(__name__)


def location_quick_reply(sender, text=None):
    if not text:
        text = get_message('location-button')
    return {
        "recipient": {
            "id": sender
        },
        "message": {
            "text": text,
            "quick_replies": [
                {
                    "content_type": "location",
                }
            ]
        }
    }


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

# Send quick replies
def send_quick_replies(sender, type, payload):
    return {
        "recipient": {
            "id": sender
        },
        "message":{
             "text":"Pick a color:",
             "quick_replies":[
                {
                    "content_type":"text",
                    "title":"Red",
                    "payload":"PICK_ONE"
                },
                {
                    "content_type":"text",
                    "title":"Green",
                    "payload":"PICK_TWO"
                }
                ]
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
    requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload)


@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode())
            sender = data['entry'][0]['messaging'][0]['sender']['id']

            print(data)

            if 'message' in data['entry'][0]['messaging'][0]:
                message = data['entry'][0]['messaging'][0]['message']

            if 'postback' in data['entry'][0]['messaging'][0]:
                # Action when user first enters the chat
                payload = data['entry'][0]['messaging'][0]['postback']['payload']
                if payload == 'begin_button':
                    message = send_text(sender, 'Hello, how are you? Lets start')
                    send_message(message)

                    payload = location_quick_reply(sender)
                    send_message(payload)

                    return 'Ok'

                # Resend the location button
                if payload == 'do_it_again':
                    payload = location_quick_reply(sender)
                    send_message(payload)


            if 'attachments' in message:
                if 'payload' in message['attachments'][0]:
                    if 'coordinates' in message['attachments'][0]['payload']:
                        location = message['attachments'][0]['payload']['coordinates']
                        latitude = location['lat']
                        longitude = location['long']

                        send_weather_info(sender, latitude=latitude, longitude=longitude)

                        if _return == 'error':
                            message = send_text(sender, get_message('error'))
                            send_message(message)
                        
                            payload = location_quick_reply(sender)
                            send_message(payload)
            else:
                text = message['text']

                for city in CITIES:
                    if text.lower() in city:
                        _return = send_weather_info(sender, city_name=text)

                        if _return == 'error':
                            message = send_text(sender, get_message('error'))
                            send_message(message)

                            # Send location button
                            payload = location_quick_reply(sender)
                            send_message(payload)

                        return 'Ok'

                # If text not in city list...
                chat_message = search_keyword(text)

                if chat_message:
                    # if found keyword, reply with chat stuff
                    message = send_text(sender, get_message('greetings'))
                    send_message(message)
                else:
                    message = send_text(sender, get_message('greetings'))
                    send_message(message)
                    
                    #message = send_text(sender, get_message('not-a-city'))
                    #send_message(message)

                # Send location button
                payload = location_quick_reply(sender)
                send_message(payload)
        except Exception as e:
            print(traceback.format_exc())
    elif request.method == 'GET':
        if request.args.get('hub.verify_token') == os.environ.get('VERIFY_TOKEN'):
            return request.args.get('hub.challenge')
        return "Wrong Verify Token"
    return "Nothing"

if __name__ == '__main__':
    app.run(debug=True)
