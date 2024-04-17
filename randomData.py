import random
from datetime import datetime, time, timezone, timedelta
def updateDate(data):
    indexBD = 0
    indexBT = 0
    indexED = 0
    indexET = 0
    indexBegin = 0
    indexEnd = 0
    indexTimezone = 0
    for ind,y in enumerate(data[0]):
      if y =='BD':
        indexBD = ind
      if y =='BT':
        indexBT = ind
      if y =='ED':
        indexED = ind
      if y =='ET':
        indexET = ind
      if y =='DateBegin':
        indexBegin = ind
      if y =='DateEnd':
        indexEnd = ind
      if y =='TimeZone':
          indexTimezone = ind
    for row in data[2:]:
      timezon = 0
      if row[indexTimezone]=='Московское время':
          row[indexTimezone]=0
      if row[indexTimezone]!='':
        timezon = int(row[indexTimezone])
      if timezon ==0:
        timezon = '+03:00'
      else:
        bb = str(timezon)
        if bb[0]=='-':
          timezon =bb[0]+'0'+bb[1:]+':00'
        else:
          timezon ='+'+'0'+bb+':00'
          
      if row[indexBD]!='':
        if row[indexBT]=='':  
            dateB = row[indexBD] 
            dateB = datetime.strptime(dateB,"%d.%m.%Y")
        elif row[indexBT]!='': 
            dateB = row[indexBD]  +'/'+ row[indexBT]
            dateB = datetime.strptime(dateB,"%d.%m.%Y/%H:%M:%S")
        dateB = dateB.isoformat()+timezon
        row[indexBegin]  = dateB
        
      if row[indexED]!='':
        dateE = row[indexED] +'/'+ row[indexET]
        try:
            dateE = datetime.strptime(dateE,"%d.%m.%Y/%H:%M:%S")
            dateE = dateE.isoformat()+timezon
            row[indexEnd]  = dateE
        except ValueError:
            print('Это не дата. Выходим.')
        
    return data
def randomizer(data):

    zagolovok = data[0]
    indexTitleSpintax = 0       
    indexDescriptionSpintax = 0
    indexPriceSpintax = 0
    indexTitle = 0       
    indexDescription = 0
    indexPrice = 0
    for ind,row in enumerate(zagolovok):
        if row=="TitleSpintax":
            indexTitleSpintax = ind
        elif row=="DescriptionSpintax":
            indexDescriptionSpintax = ind
        elif row=="PriceSpintax":
            indexPriceSpintax = ind
        elif row=="Title":
            indexTitle = ind
        elif row=="Description":
            indexDescription = ind
        elif row=="Price":
            indexPrice = ind
        
    # print(len(data[2:]))
    for ind,row in enumerate(data[2:]):
        # рандом названия
        if row[0]=='111':
            print()
        # print(ind)
        title = row[indexTitle]
        if title=='':
            if row[indexTitleSpintax]!='':
                title = ''
                spintax = row[indexTitleSpintax]
                newTxt = str(spintax).split('{')
                for rowTxt in newTxt:
                    if rowTxt.find('}')>0:
                        newTxt2= str(rowTxt).split('}')
                        arr = str(newTxt2[0]).split('|')
                        if len(arr)>0:
                            text = randomSpintax(arr)
                            title = title + text 
                            # print(newTxt2[1])
                            if newTxt2[1]=='':
                                title = title
                            elif newTxt2[1][0]==" " or "!" or "." or '\'' or '':
                                title = title + newTxt2[1]
                            else:
                                title = title +' '+ newTxt2[1]
                    else:
                        title = title + rowTxt

                row[indexTitle] = title
            # рандом цены
        price = row[indexPrice]
        if price=='' or price==0:
            spintax = row[indexPriceSpintax]
            if spintax!='':
                price = ''
                spintax = row[indexPriceSpintax]
                newTxt = str(spintax).split('{')
                for rowTxt in newTxt:
                    if rowTxt.find('}')>0:
                        newTxt2= str(rowTxt).split('}')
                        arr = str(newTxt2[0]).split('|')
                        if len(arr)>0:
                            text = randomSpintax(arr)
                            price = price + text 
                            # print(newTxt2[1])
                            if newTxt2[1]=='':
                                title = price
                            elif newTxt2[1][0]==" " or "!" or "." or '\'' or '':
                                price = price + newTxt2[1]
                            else:
                                price = price +' '+ newTxt2[1]
                    else:
                        price = price + rowTxt

                row[indexPrice] = price
        
        # рандом описания
        if row[indexDescription]=='':
            spintax = row[indexDescriptionSpintax]
            if spintax!='':
                arr = []
                description = ""
                newTxt = str(spintax).split('{')
                for rowTxt in newTxt:
                    if rowTxt.find('}')>0:
                        newTxt2= str(rowTxt).split('}')
                        arr = str(newTxt2[0]).split('|')
                        if len(arr)>0:
                            text = randomSpintax(arr)
                            description = description + text 
                            # print(newTxt2[1])
                            if newTxt2[1]=='':
                                description = description
                            elif newTxt2[1][0]==" " or "!" or "." or '\'' or '':
                                description = description + newTxt2[1]
                            else:
                                description = description+' '+ newTxt2[1]
                    else:
                        description = description + rowTxt
                # print('zz',description.find('%Заголовок%'))
                if description.find('%Заголовок%')>=0:
                    description = description.replace('%Заголовок%',title)
                if description.find('%Цена%')>=0:
                    description = description.replace('%Цена%',price) 
                row[indexDescription] = description
    data = updateDate(data)
    return data

def randomSpintax(arr):
    length = len(arr)
    rrr = random.randint(0,length-1)
    return arr[rrr]