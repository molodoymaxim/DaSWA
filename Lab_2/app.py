import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, send_from_directory
import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1488@db:5432/postgres'

db = SQLAlchemy(app)

class ManagerPassword(db.Model):
    __tablename__ = 'manager_password'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    password = db.Column(db.String(255))
    description = db.Column(db.String(255))

# Создание таблицы, если она не существует
def create_table():
    with app.app_context():
        db.create_all()

# Конфигурация базы данных PostgreSQL
def connect():
    conn = psycopg2.connect(
        host='db',
        port='5432',
        database='postgres',
        user='postgres',
        password='1488'
    )
    return conn
# Главная страница
@app.route('/')
def index():
    passwords = ManagerPassword.query.all()
    return render_template('index.html', passwords=passwords)

# Сохранение пароля и текста
@app.route('/save', methods=['POST'])
def save():
    password = request.form['password']
    description = request.form.get('description')

    if not description:
        description = 'null'

    new_password = ManagerPassword(password=password, description=description)
    db.session.add(new_password)
    db.session.commit()

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
