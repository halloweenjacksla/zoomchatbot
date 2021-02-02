import os
import json
import requests

def auth(event, context):
  r = requests.get('https://zoom.us/launch/chat?jid=robot_' + os.getenv('zoom_bot_jid'), allow_redirects=True)
  resp = {
    'statusCode': 200,
    'body': 'Thank you for installing Cirrus Logic IT Helper'
  }
  return resp

def deauth(event, context):
  
  resp = {
    'statusCode': 200,
    'body': "This is a deauth"
  }
  return resp
