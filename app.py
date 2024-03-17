from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users20.db'
app.config['SECRET_KEY'] = 'gfdgdf'
db = SQLAlchemy(app)

# объект миграции
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100))
    age = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        print(username, email)

        existing_user = User.query.filter_by(email=email).first()
        existing_user2 = User.query.filter_by(username=username).first()
        if not (existing_user or existing_user2):
        # Создание нового объекта пользователя
            new_user = User(username=username, email=email, password=password)

            # Добавление пользователя в базу данных
            db.session.add(new_user)
            db.session.commit()

            # Создание профиля для пользователя
            new_profile = Profile(user_id=new_user.id)
            db.session.add(new_profile)
            db.session.commit()
            flash('Успешная регистрацтя', category='success')
            return redirect(url_for('index'))
        else:
            flash('Invalid register!', category = 'error')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Здесь будет ваша логика аутентификации
    return render_template('login.html')


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/wheel1')
def wheel1():
    return render_template('wheel1.html')

@app.route('/wheel2')
def wheel2():
    return render_template('wheel2.html')

if __name__ == '__main__':
    app.run(debug=True)
