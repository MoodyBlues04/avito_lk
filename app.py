from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import hashlib
import os
import googleSheets
import timeWeb
import updateSheet


app = Flask(__name__)
app.secret_key = 'your_secret_key440055'  # Замените на ваш секретный ключ

path_to_save_images = os.path.dirname(os.path.abspath(__file__))
path_to_save_images = os.path.join(path_to_save_images,'database.db')


def get_db_connection():
    conn = sqlite3.connect(path_to_save_images)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def home():
    return 'Добро пожаловать на главную страницу!'

@app.route('/landing')
def landing():
    return render_template('landing.html')


@app.route('/process_registration', methods=['POST'])
def process_registration():
    # Получаем данные из запроса POST
    email = request.form['email']
    password = request.form['password']
    return 'Регистрация успешно завершена!'


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/adm_login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        # print(user)

        if user and user['password'] == hashed_password:
            session['user_id'] = user['id']
            # print('yes')
            return redirect(url_for('admin_panel'))

        else:
            error = 'Неправильное имя пользователя или пароль'

    return render_template('login_adm.html', error=error)


@app.route('/')
def index():
    return redirect(url_for('admin_login'))


@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('index'))


@app.route('/update_content', methods=['POST'])
def update_content():

    content_id = request.form['id']
    short_title = request.form['short_title']
    client_secret_Avito = request.form['client_secret_Avito']
    client_id_Avito = request.form['client_id_Avito']
    tokenTimeWeb = request.form['tokenTimeWeb']
    path = request.form['path']
    if request.form.get('active') == None:
        active = 0
    else:
        active = 1
    
    bucket = request.form.get('selbucket')
    # path = rootPath.path()
    conn = sqlite3.connect(path_to_save_images)
    cursor = conn.cursor()
    # print (bucket)
    if bucket=='':
        cursor.execute('UPDATE content SET short_title=?, client_id_Avito=?, client_secret_Avito=?, tokenTimeWeb=?, active=?,path=?  WHERE id=?',
                       (short_title, client_id_Avito, client_secret_Avito, tokenTimeWeb,active,path, content_id))
    else:
        cursor.execute('UPDATE content SET short_title=?, client_id_Avito=?, client_secret_Avito=?, tokenTimeWeb=?, active=?, bucket=?,path=? WHERE id=?',
                       (short_title, client_id_Avito, client_secret_Avito, tokenTimeWeb,active, bucket,path, content_id))    
    conn.commit()
    conn.close()

    return redirect(url_for('admin_panel'))


@app.route('/delete_content', methods=['POST'])
def delete_content():
    short_title = request.form['short_title']
    # path = rootPath.path()
    conn = sqlite3.connect(path_to_save_images)
    cursor = conn.cursor()
    print(short_title)
    cursor.execute('DELETE FROM content WHERE short_title = (?)', (short_title, )) 
    conn.commit()
    conn.close()
    return redirect(url_for('admin_panel'))


@app.route('/create_content', methods=['POST'])
def create_content():
    newTable = googleSheets.createNewTable()
    client_secret_Avito = ''
    client_id_Avito = ''
    tokenTimeWeb = ''
    url = newTable[1]
    # path = rootPath.path()
    conn = sqlite3.connect(path_to_save_images)
    cursor = conn.cursor()
    length = conn.execute('SELECT * FROM content').fetchall()
    length = length[-1][00]
    short_title = 'Новая таблица' + str(length+1)
    idblock = 'cards' + str(length+1)
    active = 0
    path = '/'
    # if file:
    #     cursor.execute('UPDATE content SET short_title=?, img=?, altimg=?, title=?, tokenTimeWeb=? WHERE id=?',
    #                (short_title, imgpath, altimg, title, tokenTimeWeb, content_id))
    # else:
    row = idblock, short_title, path ,client_id_Avito, client_secret_Avito, tokenTimeWeb, '',active,'', url
    print (row)
    cursor.execute('INSERT INTO content (idblock, short_title, path, client_id_Avito, client_secret_Avito, tokenTimeWeb, bucket, active, sheetId, url) VALUES (?,?,?,?,?,?,?,?,?,?)',    (row))
    conn.commit()
    conn.close()

    return redirect(url_for('admin_panel'))


@app.route('/admin_panel')
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('admin_login'))

    conn = get_db_connection()
    blocks = conn.execute('SELECT * FROM content').fetchall()  # Получаем все записи из таблицы content
    conn.close()
    
    # Преобразование данных из БД в список словарей
    blocks_list = [dict(ix) for ix in blocks]
    # print(blocks_list) [{строка 1 из бд},{строка 2 из бд},{строка 3 из бд}, строка 4 из бд]

     # Теперь нужно сделать группировку списка в один словарь json
    # Группировка данных в словарь JSON
    json_data = {}
    for raw in blocks_list:
        # print (raw['tokenTimeWeb'])
        if raw['tokenTimeWeb']!='':
            bucketsAll = timeWeb.listBucket(raw['tokenTimeWeb'])
        else:
            bucketsAll = []
        buckets = []
        for y in bucketsAll:
            buckets.append(y['name'])
        # print (buckets)
        # Создание новой записи, если ключ еще не существует
        if raw['idblock'] not in json_data:
            json_data[raw['idblock']] = []
        if raw['active']==1:
            active = '1'
        elif raw['active']==0:
            active = '0'
        # Добавление данных в существующий ключ
        json_data[raw['idblock']].append({
            'id': raw['id'],
            'short_title': raw['short_title'],
            # 'img': raw['img'],
            'client_id_Avito': raw['client_id_Avito'],
            'client_secret_Avito': raw['client_secret_Avito'],
            'tokenTimeWeb': raw['tokenTimeWeb'],
            'active': active,
            'buckets':buckets,
            'bucket': raw['bucket'],
            'url': raw['url'],
            'path': raw['path']
        })

    # print(json_data)
    # передаем на json на фронт - далее нужно смотреть admin_panel.html и обрабатывать там
    return render_template('admin_panel.html', json_data=json_data)


@app.route('/update_table', methods=['POST'])
def update_table():
    url = request.form['url']
    updateSheet.update(url)
    return redirect(url_for('admin_panel'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
    
