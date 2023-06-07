import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, send_from_directory
import psycopg2
app = Flask(__name__)

# Конфигурация базы данных PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'postgres'
db_user = 'postgres'
db_password = '1488'

# Установление соединения с базой данных
def connect():
    conn_str = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    conn = psycopg2.connect(conn_str)
    return conn

# Главная страница
@app.route('/')
def index():
    conn = connect()
    cursor = conn.cursor()

    # Получение всех паролей из базы данных
    cursor.execute('SELECT * FROM public.manager_password')
    passwords = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', passwords=passwords)

# Сохранение пароля и текста
@app.route('/save', methods=['POST'])
def save():
    password = request.form['password']
    description = request.form.get('description')

    if not description:
        description = 'null'

    conn = connect()
    cursor = conn.cursor()

    # Вставка нового пароля и текста в базу данных
    cursor.execute('INSERT INTO manager_password (passwords, description) VALUES (%s, %s)', (password, description))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/success')

# Страница успешного добавления пароля
@app.route('/success')
def success():
    return render_template('success.html')

# Предоставление статических файлов (например, CSS и JavaScript)
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.getcwd()
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
