import sys, json, requests
from flask import Flask, request, Response
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
app = Flask(__name__)
PAT = 'EAACh9MQ3zy8BAJuw2AdCaSezuGIio39aVlFENWK1ZA0LHVEcU3BnhqFRrUJrZAKEfCdp9DZBJa8UAZB0ZCFb7FWtJ6mZAzUVenZCzEcJX8vg7HxEAwgcL93YOfXxZCb9CJygQpMo8J49JR6AGYh67CeoMGZAAs9OZCsUPrhhA19wFmlAZDZD'
VERIFY_TOKEN = 'test'


@app.route('/', methods=['GET'])
def handle_verification():
    '''
    Verifies facebook webhook subscription
    Successful when verify_token is same as token sent by facebook app
    '''
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        logger.info("\\n succefully verified")
        return Response(request.args.get('hub.challenge', ''))
    else:
        logger.info("Wrong verification token!")
        return Response('Error, invalid token')


@app.route('/', methods=['POST'])
def handle_message():
    '''
    Handle messages sent by facebook messenger to the applicaiton
    '''
    data = request.get_json()
    logger.info("\\n")

    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    recipient_id = messaging_event["recipient"]["id"]
                    message_text = messaging_event["message"]["text"]
                    send_message(sender_id, message_text)
                    #send_message_response(sender_id, parse_user_message(message_text))
    logger.info(message_text)
    logger.info("\\n")
    logger.info(sender_id)
    return "ok"


def send_message(sender_id, message_text):
    '''
    Sending response back to the user using facebook graph API
    '''
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
        params={"access_token": PAT},
        headers={"Content-Type": "application/json"},
        data=json.dumps({
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }))


def send_message_response(sender_id, message_text):

    sentenceDelimiter = ". "
    messages = message_text.split(sentenceDelimiter)
    for message in messages:
        send_message(sender_id, message)


def send_to_apiai():
    '''
    This function should send the received message from google_translate
    and send it to api.ai. The function should return an api.ai response with
    intents
    '''
    pass


def retrive_faq():
    '''
    This function would retrieve the faqs based on intent
    '''
    pass


def translate_google():
    '''
    this function will translate the received text using google translate
    '''
    pass


def normalize_dictionary():
    '''
    use the roman urdu dictionary to normlize text and return a normalized value
    '''
    pass


if __name__ == '__main__':
    app.run(port=80)
