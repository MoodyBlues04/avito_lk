import mysql.connector

# Укажите данные для подключения к базе данных
mydb = mysql.connector.connect(
  host="147.45.144.91",
  user="gen_user",
  password="tSQ1X0:zTfmqAb",
  database="Users"
)

# Проверка соединения
if mydb.is_connected():
    print("Успешное подключение к базе данных")
