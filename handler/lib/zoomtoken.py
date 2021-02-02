import boto3
import os
import requests
from datetime import datetime, timedelta
from base64 import b64encode


client = boto3.resource('dynamodb')
tokentable=client.Table(os.getenv('ZOOM_TOKEN_TABLE'))


def getNewZoomToken():
  clientid=os.getenv('zoom_client_id')+':'+os.getenv('zoom_client_secret')
  clientauthorization = b64encode(clientid.encode('ascii'))
  tokenheaders = {
    "Authorization": "Basic " + clientauthorization.decode('utf-8'),
  }
  
  try:
    r = requests.post('https://zoom.us/oauth/token?grant_type=client_credentials',headers=tokenheaders)
    return r.json()['access_token']
  except requests.ConnectionError as e:
    print("Couldn't connect to zoom to get a token")
    print(str(e))
  except requests.Timeout as e:
    print("Connection to zoom timed out.")
    print(str(e))
  except requests.RequestException as e:
    print("There was an error.")
    print(str(e))


def insertTokenDynamodb(accesstoken):
  expires=int(datetime.now().timestamp()) + 3600

  resp = tokentable.put_item(
    Item={
      'zoomToken':accesstoken,
      'expires':expires,
    }
  )


def getZoomToken():
  resp = tokentable.scan(
  )
  if resp['Items'] == 0 :
    zoomtoken = getNewZoomToken()
    insertTokenDynamodb(zoomtoken)
  else:
    token = resp['Items'][0]
    if int(datetime.now().timestamp()) >= token['expires'] :
      deleteZoomToken(token)
      zoomtoken = getNewZoomToken()
      insertTokenDynamodb(zoomtoken)
    else:
      zoomtoken = token['zoomToken']

  return zoomtoken


def deleteZoomToken(token):
  resp = tokentable.delete_item(
    Key={
      'zoomToken': token['zoomToken']
    }
  )
