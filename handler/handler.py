import json
import os
import sys
sys.path.append("/var/task/handler/lib")
import commands

def hello(event, context):
  body = {
      "message": "Welcome to the Cirrus IT Helper Bot",
  }

  response = {
      "statusCode": 200,
      "body": json.dumps(body)
  }

  return response

def cirrusithelp(event, context):

  zoomevent = json.loads(event['body'])
  if zoomevent['payload']['robotJid'] == os.getenv('zoom_bot_jid') :
    if zoomevent['event'] == 'bot_installed':
      body = {
        'robot_jid': zoomevent['payload']['robotJid'],
        'to_jid': zoomevent['payload']['userId'],
        'account': zoomevent['payload']['accountId'],
        'content': {
            'head': {
                'text': "Welcome to the Cirrus IT Helper Bot"
            },
            'body': [{
                'type': 'message',
                'text': 'Thank you for installing Cirrus IT Helper Bot'
            }]
          }
      }
    elif zoomevent['event'] == 'bot_notification' and zoomevent['payload']['cmd'] == 'hello':
        commands.sendHello(zoomevent['payload'])
 
  return {
      'statusCode': 201,
      'body': json.dumps(body)
  }
