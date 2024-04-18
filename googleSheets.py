import gspread
from gspread import utils
from datetime import datetime, time, timezone, timedelta
import json

with open('credentials.json') as credentials_file:
    credentials = json.load(credentials_file)
gc = gspread.service_account_from_dict(credentials)


# print(sh.sheet1.get('A1:B100'))

  
def createNewTable():
  #  email = 'eliseevvp@gmail.com'
   email =  'vl.kaminskijj@gmail.com' 
  #  sh = gc.create('Новая Таблица Avito')
   sh = gc.copy('1lQ_XS4nAeQqsL_se1D9dfl9kFl3gbgxmLp-wr3qU00A','Новая Таблица Avito')
   sh.share(email, perm_type='user', role='writer')
  #  sh.share('eliseevvp@gmail.com', perm_type='user', role='writer')
   listPermission = sh.list_permissions()
   
   id = ''
   for row in listPermission:
     if row['emailAddress'] == email:
       id = row['id']
   sh.transfer_ownership(id)
   return [sh.id,sh.url] 

def getDataFromWS(url):
    sh = gc.open_by_url(url)
    worksheet = sh.worksheet('Объявления')
    list_of_lists = worksheet.get_all_values()
    print("Получено",len(list_of_lists),len(list_of_lists[0]))
    return list_of_lists
  
def updateWS(url,data):
    # data = []
    # deleteRowsAdres =  utils.rowcol_to_a1 (len(data2),len(data2[0]))
    # for row in data2:
    #   for element in row:
    #     if element!='' :
    #       data.append(row)
    #       break
    sh = gc.open_by_url(url)
    worksheet = sh.worksheet('Объявления')
    print('результат - строк:',len(data),'столбцов',len(data[0]))
    if len(data)>1 and len(data[0])>0:
        adres =  utils.rowcol_to_a1 (len(data),len(data[0]))
        adres = 'A1:'+adres
        # worksheet.clear()
        worksheet.row_count
        worksheet.update(adres, data)
        if len(data) == worksheet.row_count:
            worksheet.delete_rows(len(data),worksheet.row_count)
        else:
            worksheet.delete_rows(len(data)+1,worksheet.row_count)
        worksheet.add_rows(10)
        # worksheet.delete_rows()
    
# createNewTable()
# Open a sheet from a spreadsheet in one go
# wks = gc.open("Where is the money Lebowski?").sheet1

# # Update a range of cells using the top left corner address
# wks.update('A1', [[1, 2], [3, 4]])

# # Or update a single cell
# wks.update('B42', "it's down there somewhere, let me take another look.")

# # Format the header
# wks.format('A1:B1', {'textFormat': {'bold': True}})
# createNewTable()
