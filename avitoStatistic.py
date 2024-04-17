import requests 
import json
import sqlite3
from requests.utils import requote_uri
from datetime import datetime, timezone, timedelta

def requestGet(url,token,status):
    fin = False
    page =1
    result = []
    while (fin ==False): 
        urlT = url

        if status=='all':
            urlT=urlT+'?per_page=100'+'&page='+str(page)+'&status=active,removed,old,blocked,rejected'
        # let urlEncoded = encodeURI(urlT) 
        headers = {    
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' +token
        }   

        response  =  requests.get(urlT,headers = headers) 
        res = json.loads(response.content)   
        # //   const content = response.getAllHeaders() 
        # //   const code = response.getResponseCode()
        # let text =JSON.parse(response.getContentText())
        # // if(text.result.status==false) {
        # //   console.log(text.result)
        # // }
        if len(res['resources'])<100:
            fin = True
        page = page + 1
        
        result = result + res['resources']

    
    return result

def getUser(token):
    url = 'https://api.avito.ru/core/v1/accounts/self'
    headers = {    
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +token
    }   
    response  =  requests.get(url,headers = headers) 
    res = json.loads(response.content)  
    return res

def getStat(list,dateB,dateE,token):
    user = getUser(token)
    avitoID = []
    for row in list:
        avitoID.append(row['id'])
    avitoID200 = []
    while(len(avitoID)>0):
        rows200 = avitoID[:200]
        del(avitoID[:200])
        avitoID200.append(rows200)
    url = 'https://api.avito.ru/stats/v1/accounts/'+ str(user['id']) +'/items'
    result = []
    headers = {    
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +token
    }  
    for r200 in avitoID200:
        ok = False
        while (ok==False):
            data = json.dumps({
            "dateFrom": dateB,
            "dateTo": dateE,
            "itemIds": r200,
            "periodGrouping": "month"            
            })            
            response  =  requests.post(url,data=data,headers = headers) 
            ok = response.ok
            if ok==False:
                dateB = ""
                dateE = ""
        res = json.loads(response.content)
        res = res['result']['items']
        result = result + res
    return result

def getLastReports(token):
    url = 'https://api.avito.ru/autoload/v2/reports/last_completed_report'
    headers = {    
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' +token
    }
    response = requests.get(url=url,headers=headers)  
    res = json.loads(response.content)
    return res

def getIds(list,token):
    avitoID50 = []
    while(len(list)>0):
        rows50 = list[:50]
        del(list[:50])
        avitoID50.append(rows50)
    result = []
    for r50 in avitoID50:
        string =','.join(str(el) for el in r50)
        url = 'https://api.avito.ru/autoload/v2/items/ad_ids' +'?query='+ string
        headers = {    
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' +token
        }
        response = requests.get(url=url,headers=headers)  
        res = json.loads(response.content)
        result = result +res['items']
            
    return result

def getStatistic(token):
    url = 'https://api.avito.ru/core/v1/items'
    list =  requestGet(url,token,"all")
    # list = json.loads(result.content)
    # print('Получили Объявления')
    yesterday = datetime.today() - timedelta(days=270)
    dateB = datetime.today() 
    dateE = datetime.today() - timedelta(days=150)
    dateB = dateB.strftime("%Y-%m-%d")
    dateE = dateE.strftime("%Y-%m-%d")
    stats = getStat(list,dateB,dateE,token)
    # print('Получили статистику')
    lastReport = getLastReports(token)
    # print(lastReport)
    
    autoloadFinishedAt = lastReport['finished_at'][:10]
    if autoloadFinishedAt =="":
        autoloadFinishedAt = lastReport['started_at'][:10]
    # print('Получили последний отчет '+str(autoloadFinishedAt))
    uniq=[]
    for i in list:
        uniq.append(i['id'])
    ids = getIds(uniq,token)
    # print('Получили IDS')
    result = []
    for i in list:
        status = ''
        if i['status'] == 'active':
            status='Добавлено'
        elif i['status'] == 'removed':
            status='Удалено'
        elif i['status'] == 'rejected':
            status='Другие ошибки'
        elif i['status'] == 'blocked':
            status='Заблокировано'
        elif i['status'] == 'old':
            status='Старое'
        elif status =='':
            status = i['status']
        link = 'https://www.avito.ru/items/' +str(i['id'])
        res = filter(lambda it: it['itemId'] == i['id'], stats)
        
        ad_id = filter(lambda it: it['avito_id'] == i['id'], ids)
        uniqViews270	= 0
        uniqContacts270	= 0
        uniqFavorites270= 0
        for res0 in ad_id:
            adid = res0['ad_id']
        
        for res0 in res:
            for r in res0['stats']:
                uniqViews270 = uniqViews270 + r['uniqViews']
                uniqContacts270 = uniqContacts270 + r['uniqContacts']
                uniqFavorites270 = uniqFavorites270 + r['uniqFavorites']
        result.append([
            i['status'],
            status,
            i['id'],
            link,
            autoloadFinishedAt,
            uniqViews270,
            uniqContacts270,
            uniqFavorites270,
            adid
        ])
    return result
 
    