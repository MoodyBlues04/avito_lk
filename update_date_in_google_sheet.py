import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# Подключение к Google Sheets
scope = ['https://docs.google.com/spreadsheets/d/1gc--2I3Xzq7egI1sG42ktUCmLX6ZoBbx96OkkGCpalg/edit#gid=2077348259']
creds = ServiceAccountCredentials.from_json_keyfile_name('/root/avitoWebGoogleTab/erudite-spot-412112-513de6a60c81.json', scope)
client = gspread.authorize(creds)

# Открытие Google таблицы
sheet = client.open('шторкин').sheet1

# Получение данных из столбцов "Избранное" и "Дата"
favorite_column = sheet.find('UniqFavorites270').col
date_column = sheet.find('BD').col
values = sheet.get_all_values()

# Обновление данных
for row in range(2, len(values)+1):
    if int(values[row-1][favorite_column-1]) >= 3:
        sheet.update_cell(row, date_column, str(date.today()))

print('Дата успешно обновлена в указанных строках.')
