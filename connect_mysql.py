#!/usr/bin/env python3
import MySQLdb

try:
    db = MySQLdb.connect(
        host="147.45.144.91",
        user="gen_user",
        passwd="tSQ1X0:zTfmqAb",
        db="default_db",
        port=3306
    )

    cursor = db.cursor()

    # Выполнение SQL запросов
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s" % data)

    # Закрытие соединения
    db.close()

except MySQLdb.Error as e:
    print("Ошибка подключения к базе данных MySQL:", e)
