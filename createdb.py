# import sqlite3

# # Создание или подключение к базе данных
# conn = sqlite3.connect('/home/root/database.db')

# # Создание курсора
# c = conn.cursor()

# # Создание таблицы Content
# c.execute('''CREATE TABLE IF NOT EXISTS content (
#              id INTEGER PRIMARY KEY AUTOINCREMENT,
#              idblock TEXT,
#              short_title TEXT,
#              path TEXT,
#              client_id_Avito TEXT,
#              client_secret_Avito TEXT,
#              tokenTimeWeb TEXT,
#              bucket TEXT,
#              active BOOLEAN,
#              sheetId TEXT,
#              url TEXT)''')

# # Создание таблицы Users
# c.execute('''CREATE TABLE IF NOT EXISTS users (
#              id INTEGER PRIMARY KEY AUTOINCREMENT,
#              username TEXT,
#              password TEXT)''')

# # Закрытие соединения с базой данных
# conn.close()
