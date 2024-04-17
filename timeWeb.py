import requests 
import json
import sqlite3
from requests.utils import requote_uri

def listBucket(token):
    # token = 'eyJhbGciOiJSUzUxMiIsInR5cCI6IkpXVCIsImtpZCI6IjFrYnhacFJNQGJSI0tSbE1xS1lqIn0.eyJ1c2VyIjoidngyMTYxMiIsInR5cGUiOiJhcGlfa2V5IiwicG9ydGFsX3Rva2VuIjoiNjM5MDYzOTktZjk0Yy00MTQ0LTk1YTQtZjZhNGMxMDEzNGI0IiwiYXBpX2tleV9pZCI6IjQzMzJkYzg4LTczNTctNDBmYi1iNzYyLThkZjc4YjRmYTAyNSIsImlhdCI6MTcwNTA1NzQxN30.X82y3EyOtaNbhFveEcgAi56jbO1LsjMIQP13wQqQJ7lezR9M2JJ-mUuK1cJKPpoRuWz36z-UKEDT9VKLLPJ-8X9TqMnX6T7k1H-mRB5XmbQItNfvc0m39CZde9L4OOC7fpscSIDYy0ctOQDciLJfBugNbYe_8bzMad_8653coGYjyoRZ3I3LnfsSLT0-qaIkfk7dAZ3jNB4j1cjxw9SZ0xB3Qt0fWmlFqbcO6DRuL1TB2vl02R_cdLTqJTj6te3KsTZ552q8js6b9PZR2zSIPqKgdGV48vbdk5yunVyem-24nUh9VVQMEgVkmhXlMBbtxW2op4sfJV4OdwpgeBHaoL61x01xA9HlBHqOZX-c20eC9e2nVymDQF0r7OIokkZGlDz9hdZVttBDodV8XwMw25biQt7Iwp_ecd0yat3vp867J3oo_tDZuetx2nVp9F8rzBaS7h9VLFHkA3Kc5x3abs23P1WmspT711CAhN6YAtI6WFJ0OwEQw-vcq8KJqISw'
    url = 'https://api.timeweb.cloud/api/v1/storages/buckets'
    headers =  {
           'Authorization':'Bearer '+token,
           }
    result =  requests.get(url,headers = headers)
    res = json.loads(result.content)
    try: 
        if result.status_code==200:  
            try:
                res = res['buckets']
            except KeyError:
                res = []
        elif result.status_code==403:
            res = 'forbidden'
        else:
            res = []
    except:
        res=[]
   

    return res

def getListFiles(root,token,butId):
    url = 'https://api.timeweb.cloud/api/v1/storages/buckets/'+str(butId['id'])+'/object-manager/list'
    if root == '': 
        url = url + '?prefix=/'
    else: 
        if root[-1]!='/':
            root=root+'/'
        if root[0]=='/':
            root= root[1:]
        url = url + '?prefix='+root
    headers =  {
           'Authorization':'Bearer '+token,
           }
    url = requote_uri(url)
    result =  requests.get(url,headers = headers)
    res = json.loads(result.content)  
    return res
 
def getFoldersTW(rootPath,token,bucket):
    bucketIds = listBucket(token)
    if bucketIds =='forbidden':
        print('неверный токен TW')
        listFilesResult = 'error token'
    else:
        bucketId = list(filter(lambda it: it['name'] == bucket, bucketIds))[0]
        bucketName = bucketId['name']
        host =  bucketId['hostname']
        listfolders = getListFiles(rootPath,token,bucketId)
        listFilesResult = []
        for index,row in enumerate(listfolders['files']):
            listFiles = getListFiles(row['key'],token,bucketId)
            files = []
            for file in listFiles['files']:
                url = 'https://'+ host+'/'+bucketName+'/'+file['key']
                files.append(url)
            name = str(row['key']).split('/')
            newRow={
                    '№':index,
                    'name': name[-1],
                    'path': row['key'],
                    'files':files,
                    'use': False
                
            }
            listFilesResult.append(newRow)
    return listFilesResult
    


    


