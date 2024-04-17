import timeWeb
import json
import sqlite3
import googleSheets
import randomData
import avitoOAuth
import avitoStatistic
import os

path_to_save_images = os.path.dirname(os.path.abspath(__file__))
absolute_path = os.path.join(path_to_save_images,'database.db')
def get_db_connection(url):
    # print (23,absolute_path)
    # if os.path.exists(absolute_path):
    #     print('File exists')
    # print (2,ROOT_DIR+'\\database.db')
    conn = sqlite3.connect(absolute_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # print('ttttttt',cursor.fetchall())
    conn.row_factory = sqlite3.Row
    if url=='all':
        blocks = conn.execute('SELECT * FROM content WHERE active=1').fetchall()  # Получаем все записи из таблицы content
        conn.close()
    else:
        string = 'SELECT * FROM content WHERE url="' +str(url) +'"'
        # string = 'SELECT * FROM content WHERE url="https://docs.google.com/spreadsheets/d/1GW7F40ftwATgU3--sDDGM02Fp0wpM-x_0KFMmwJSAlI"'
        blocks = conn.execute(string).fetchall()  # Получаем все записи из таблицы content
        conn.close()
    blocks_list = [dict(ix) for ix in blocks]
    return blocks_list


def update(url):
    print('обновляем таблицу',url)
    blocks_list = get_db_connection(url)
    for raw in blocks_list:
        print(raw['client_id_Avito'],raw['client_secret_Avito'])
        if raw['client_id_Avito']!='' or raw['client_secret_Avito']!='':
            avitoToken = avitoOAuth.getToken(raw['client_id_Avito'],raw['client_secret_Avito'])
            stat = avitoStatistic.getStatistic(avitoToken)
            print('статистика получена')
        else:
            stat=[]
            print('статистика Не получена')
        data = googleSheets.getDataFromWS(raw['url'])
        if raw['tokenTimeWeb']=='' or raw['bucket']=='':
            listFiles = []
            print('список файлов не получен')
        else:
            listFiles = timeWeb.getFoldersTW(raw['path'],raw['tokenTimeWeb'],raw['bucket'])
            print('список файлов получен')
        IndexImageFolder = ''
        for ind,row in enumerate(data[0]):
            if row=="ImageFolder":
                IndexImageFolder = ind

        for row in data[2:-1]:
            spintax = row[IndexImageFolder]
            if spintax!='':
                newListFiles = list(filter(lambda it: it['name'] == spintax, listFiles))
                if len(newListFiles)>0:
                    row[IndexImageFolder-1]  = ' | '.join(newListFiles[0]['files'])
            newRow = list(filter(lambda it: it[8] == row[8], stat))
            if len(newRow)>0:
                row[0]=newRow[0][0]
                row[1]=newRow[0][1]
                row[2]=newRow[0][2]
                row[3]=newRow[0][3]
                row[4]=newRow[0][4]
                row[5]=newRow[0][5]
                row[6]=newRow[0][6]
                row[7]=newRow[0][7]
        data = randomData.randomizer(data)
        print('рандомайзер готов')
        googleSheets.updateWS(raw['url'],data)
        print('обновлена таблица')


def updateRandom():
    url = 'all'
    blocks_list = get_db_connection(url)

    for raw in blocks_list:
        data = googleSheets.getDataFromWS(raw['url'])
        print(raw['short_title'],len(data),len(data[0]))
        if len(data) >0:                   
            data = randomData.randomizer(data)
            print('рандомайзер готов',len(data),len(data[0]))
            googleSheets.updateWS(raw['url'],data)
            print('обновлена таблица')
        else:
            print('данных в таблице нет')
        
        
def updateListFiles():
    url = 'all'
    blocks_list = get_db_connection(url)
    for raw in blocks_list:
        data = []
        print("Обрабатываем таблицу", raw['short_title'])
        if raw['tokenTimeWeb']=='' or raw['bucket']=='' :
            
            print('Нет tokenTimeWeb или не указан bucket')
        else:
            data = googleSheets.getDataFromWS(raw['url'])
        if len(data) >0:   
            listFiles = timeWeb.getFoldersTW(raw['path'],raw['tokenTimeWeb'],raw['bucket'])
            if listFiles!='error token':
                print('список файлов получен')
                IndexImageFolder = ''
                for ind,row in enumerate(data[0]):
                    if row=="ImageFolder":
                        IndexImageFolder = ind
                for row in data[2:-1]:
                    spintax = row[IndexImageFolder]
                    if spintax!='':
                        newListFiles = list(filter(lambda it: it['name'] == spintax, listFiles))
                        # item = 
                        if len(newListFiles)>0:
                            row[IndexImageFolder-1]  = ' | '.join(newListFiles[0]['files'])
                googleSheets.updateWS(raw['url'],data)
                print('обновлена таблица', raw['short_title'])
            else:
                print('Неверный токен TW')
        else:
            print('данных в таблице нет')

def updateStat():
    url = 'all'
    blocks_list = get_db_connection(url)
    
    for raw in blocks_list:
        print(raw['short_title'])
        data = []
        if raw['client_id_Avito']=='':
            print('Нет id для Авито')
        else:
            data = googleSheets.getDataFromWS(raw['url'])
        if len(data) >0:
            avitoToken = avitoOAuth.getToken(raw['client_id_Avito'],raw['client_secret_Avito'])
            if avitoToken!='':
                stat = avitoStatistic.getStatistic(avitoToken)
                print('статистика получена') 
                for row in data[2:-1]:
                    newRow = list(filter(lambda it: it[8] == row[8], stat))
                    if len(newRow)>0:
                        row[0]=newRow[0][0]
                        row[1]=newRow[0][1]
                        row[2]=newRow[0][2]
                        row[3]=newRow[0][3]
                        row[4]=newRow[0][4]
                        row[5]=newRow[0][5]
                        row[6]=newRow[0][6]
                        row[7]=newRow[0][7]
                googleSheets.updateWS(raw['url'],data)
                print('обновлена таблица')
            else:
                print('неверные ключи Авито')
        else:
            print('данных в таблице нет')        
# update('all')