from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'  # Секретный ключ для защиты сессий и форм
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # URI базы данных (SQLite в данном случае)
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

# Маршруты
@app.route('/')
def home():
    return 'Добро пожаловать на главную страницу!'

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Неверные учетные данные. Пожалуйста, попробуйте снова.', 'danger')

    return render_template('login.html')

# Контекст приложения для создания таблиц
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
