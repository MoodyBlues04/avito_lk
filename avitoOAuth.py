import requests
import json
from requests_oauthlib import OAuth1Session


def getToken(client_id,client_secret):
    avito = OAuth1Session('client_key',
                            client_secret='client_secret')
    data = ''+'grant_type=client_credentials&'+'client_id='+client_id+'&'+'client_secret='+client_secret
    
    url= "https://api.avito.ru/token"
    # let options = {
    #     method : "POST",

    #     payload : data,
    #     muteHttpExceptions : true,
    headers = {    
    'Content-Type': 'application/x-www-form-urlencoded'
        }   
    # }
    response  =  avito.post(url, data=data)
    res = response.content 
    res = json.loads(res)   
    # const response = UrlFetchApp.fetch(urlEncoded, options);      
    # const content = response.getAllHeaders() 
    # const code = response.getResponseCode()
    # let text =JSON.parse(response.getContentText())
    try:
        result = res['access_token']
    except KeyError:
        result = ''
    return result

# getToken()