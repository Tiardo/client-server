from flask import Flask, render_template, request, redirect, url_for, session
from flask import send_file
from flask_mysqldb import MySQL
import hashlib
import mysql.connector
import io
import MySQLdb.cursors
import re


app = Flask(__name__, template_folder='templates')


app.secret_key = '11111'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '111'
app.config['MYSQL_DB'] = 'pythonlogin'
mysql = MySQL(app)


@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, hash_code(password),))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            return redirect(url_for('home'))
        else:
            msg = 'Неправильное Имя пользователя / Пароль!'
    return render_template('index.html', msg=msg)


@app.route('/pythonlogin/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' \
            in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Такой аккаунт уже существует'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'неверный email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Имя пользователя должно содержать только символы и цифры!'
        elif not username or not password or not email:
            msg = 'Пожалуйста, заполните форму!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, 1)', (username, hash_code(password), email,))
            mysql.connection.commit()
            msg = 'Вы успешно зарегистрировались!'
    elif request.method == 'POST':
        msg = 'Пожалуйста, заполните форму!'
    return render_template('register.html', msg=msg)


@app.route('/pythonlogin/home')
def home():
    if 'loggedin' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))


@app.route('/pythonlogin/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('login'))


@app.route('/pythonlogin/lex2', methods=['GET', 'POST'])
def lex2():
    if 'loggedin' in session:
        msg = ''
        if request.method == 'POST' and 'image1' in request.files:
            image = request.files['image1']

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM images WHERE image = %s', (image,))
            img = cursor.fetchone()

            if img:
                msg = 'Такая картинка есть'
            elif not image:
                msg = 'Пожалуйста, загрузите картинку!'
            else:
                cursor.execute('INSERT INTO images VALUES (%s)', (image.stream.read(),))
                mysql.connection.commit()
                msg = 'загрузка успешна'
        elif request.method == 'POST':
            msg = 'нет нужного файла'
        return render_template('lex2.html', msg=msg)
    return redirect(url_for('login'))


@app.route('/pythonlogin/lex', methods=['GET', 'POST'])
def lex():
    if 'loggedin' in session:
        return render_template('lex.html')
    return redirect(url_for('login'))


# imagefile #


@app.route('/pythonlogin/foto')
def foto():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM images")
    myresult = mycursor.fetchall()[0]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


@app.route('/pythonlogin/picture')
def picture():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM images")
    myresult = mycursor.fetchall()[0]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


@app.route('/pythonlogin/picture1')
def picture1():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM images")
    myresult = mycursor.fetchall()[1]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


@app.route('/pythonlogin/picture2')
def picture2():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM images")
    myresult = mycursor.fetchall()[2]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


@app.route('/pythonlogin/picture3')
def picture3():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM images")
    myresult = mycursor.fetchall()[3]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


@app.route('/pythonlogin/picture4')
def picture4():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM images")
    myresult = mycursor.fetchall()[4]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


@app.route('/pythonlogin/clear', methods=['GET', 'POST'])
def clear():
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM images")
    mysql.connection.commit()
    return render_template('lex.html')


@app.route('/pythonlogin/errorimg')
def errorimg():
    mycursor = mysql.connection.cursor()
    mycursor.execute("SELECT * FROM err")
    myresult = mycursor.fetchall()[0]
    mycursor.connection.commit()
    blob = myresult[0]
    with open("filename2.png", 'wb') as file:
        file.write(blob)
    ofname = 'filename2.png'
    response = send_file(
        io.BytesIO(blob),
        mimetype='image/png',
        as_attachment=True,
        download_name=ofname)
    return response


def hash_code(s, salt='сайт'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()


if __name__ == '__main__':
    app.run(debug=True)
