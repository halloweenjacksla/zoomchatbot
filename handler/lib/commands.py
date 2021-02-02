import json
import requests
import sys
# sys.path.append("/var/task/handler/lib")
from zoomtoken import getZoomToken

def sendHello(payload):
  btoken = getZoomToken()
  headers = {
    'Authorization': 'Bearer '+ btoken
  }
  body = {
    'robot_jid': payload['robotJid'],
    'to_jid': payload['userJid'],
    'account_id': payload['accountId'],
    'content': {
      'head': {
        'text': 'Cirrus Logic IT chatbot'
      },
      'body':[{
        'type': 'message',
        'text': "Hello "+ payload['userName'] + " I am the Cirrus Logic Chatbot.",
      }]
    }
  }
  #TODO send a message back
  requests.post('https://api.zoom.us/v2/im/chat/messages',data = json.dumps(body), headers = headers)