from flask import Flask, url_for, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import requests
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, EmailField
from wtforms.validators import DataRequired
import time
import json

CITYLIST = ['VIENNA', 'LVIV', 'AMSTERDAM', 'BARCELONA', 'BERLIN', 
        'BRATISLAVA', 'BRUSSELS', 'BUDAPEST', 'COPENHAGEN', 'DUBLIN', 
        'HELSINKI', 'LONDON', 'MADRID', 'OSLO', 'PARIS', 'PRAGUE',
        'RĪGA', 'ROME', 'STOCKHOLM', 'TALLINN', 'VILNIUS', 'WARSAW',
        'ZAGREB', 'BUCHAREST', 'HAMBURG', 'FRANKFURT', 'MUNICH', 'VENICE',
        'FLORENCE', 'MILAN', 'MONACO', 'PORTO', 'LISBON'
        ]

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cities.db'
db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    description = db.Column(db.String, unique=False, index=True)
    icon = db.Column(db.String, unique=False, index=True)
    temp = db.Column(db.String, unique=False, index=True)

    def __repr__(self):
        return f'<City {self.name}>'

class UserMessages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, index=True)
    email = db.Column(db.String, unique=False, index=True)
    text = db.Column(db.String, unique=False, index=True)

    def __repr__(self):
        return f'<User Message {self.id}>'

app.config["SECRET_KEY"] = 'asljozu9812739870z0v6uhasf9876zxvhoiauy#97A*&79812h6^&*1usaf897'
class MessageForm(FlaskForm):
    message_name = StringField('Name', validators=[DataRequired()])
    message_email = EmailField('Email address', [DataRequired()])
    message_text = TextAreaField('Text')
    message_submit = SubmitField('Submit')

@app.route('/')
def index():
    return redirect(url_for('get_weather', city='vienna'))

@app.route('/<city>')
def get_weather(city):
    
    r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=***&units=metric').json()
    try:
        weather_data = {
            'city_name': r['name'].upper(),
            'description': r['weather'][0]['description'].capitalize(),
            'icon_code': r['weather'][0]['icon'],
            'temp': round(r['main']['temp']) if round(r['main']['temp']) <= 0 else "+" + str(round(r['main']['temp'])) ,   
        }
        if weather_data["city_name"] in CITYLIST:
            weather_data['photo'] = f'/static/img/{weather_data["city_name"].lower()}.jpg'
        else:
            weather_data['photo'] = '/static/img/other.jpg'
        return render_template('weather.html', weather_data=weather_data, date=datetime.now().strftime("%a, %d %B"))
    except:
        return redirect(url_for('index'))

@app.route('/weatherpro', methods=['GET', 'POST'])
def weather_pro():
    if request.method == 'POST':
        new_city_name = request.form['new_city_name']
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={new_city_name}&appid=***&units=metric').json()

        try:
            new_city = City(name=r['name'].upper(), description=r['weather'][0]['description'].capitalize(),
            icon=r['weather'][0]['icon'], temp=round(r['main']['temp']) if round(r['main']['temp']) <= 0 else "+" + str(round(r['main']['temp'])))
            # add the new city to db
            db.session.add(new_city)
            db.session.commit()
            return redirect(url_for('weather_pro'))
        except:
            return render_template('error.html', new_city_name=new_city_name)
    
    all_cities= City.query.all()
    return render_template('weatherpro.html', cities=all_cities, date=datetime.now().strftime("%a, %d %B"))

@app.route('/weatherpro/delete/<id>')
def weather_pro_delete(id):
    city_to_delete = City.query.get(id)
    try:
        db.session.delete(city_to_delete)
        db.session.commit()
        return redirect(url_for('weather_pro'))
    except:
        return "There was an error deleting the city. Try again later."


# @app.route('/weatherpro/update/<city_name>')
# def weather_pro_update(city_name):
#     r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid=***&units=metric').json()
#     # time.sleep(3)
#     return str(round(r['main']['temp']))


@app.route('/weatherpro/updatio/<city_list>')
def weather_pro_updatio(city_list):
    new_temperatures = []
    cities = city_list.split(',')
    for city in cities:
        r = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=***&units=metric').json()
        temp = r['main']['temp']
        new_temperatures.append(temp)
    # time.sleep(3)
    print("------------------->HERE ARE NEW TEMPERATURES:", new_temperatures)
    return str(new_temperatures)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MessageForm()

    if form.validate_on_submit():
        user_message = UserMessages()
        user_message.name = form.message_name.data
        user_message.email = form.message_email.data
        user_message.text = form.message_text.data

        try:
            db.session.add(user_message)
            db.session.commit()
            return redirect(url_for('contact'))
        except:
            return 'There was an error.'
    
    return render_template('contact.html', template_form=form)


@app.route('/check-messages')
def check_messages():
    return render_template('messages.html', users=UserMessages.query.all())

@app.route('/check-messages/delete/<id>')
def check_messages_delete(id):
    msg_to_delete = UserMessages.query.get(id)
    try:
        db.session.delete(msg_to_delete)
        db.session.commit()
        return redirect(url_for('check_messages'))
    except:
        return "There was an error deleting the city. Try again later."


