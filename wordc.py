from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'postgres://piimyaoiyfmzfx:5c389132c19ba4ed0df6a522222b765240eb3d4f1cdd4a289fad335ef1bd0ee3@ec2-50-19-109-120.compute-1.amazonaws.com:5432/d9tbdnuqu7r598'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

class Counter(db.Model):
    letters = db.Column(db.String(20), primary_key=True)
    count = db.Column(db.Integer)

    def __repr__(self):
        return '<Counter {}>'.format(self.letters) 

class GetLetters(Form):
    letters = StringField('Enter letters', validators=[DataRequired()])
    submit = SubmitField('Submit')


def get_words(letter_list, dictionary_name):
        lst = list()
        sort_lst = list()
        
        fhand = open(dictionary_name)

        for line in fhand:
            line = line.rstrip()
            lst.append(line)
        
        for item in lst:
            test = list(letter_list)
            count = 0
            for character in item:
                if character in test:
                    count = count + 1
                    test.remove(character)
            if count == len(item) and len(item)>=3:
                sort_lst.append(item)
        return sort_lst
    
def savequery(letters):
    u = Counter.query.get(letters)
    if u != None:
        u.count = u.count + 1
        db.session.commit()
    else:
        u = Counter(letters=letters, count=1)
        db.session.add(u)
        db.session.commit()
	
@app.route('/')	
@app.route('/wordcookies', methods=['GET', 'POST'])
def wordcookies():
	try:
		form = GetLetters()
		if form.validate_on_submit():
			lst = list()
			n = 0
			savequery(form.letters.data.upper())
			print (form.letters.data.upper())
			for letter in form.letters.data:
				lst.append(letter.upper()) #makes list of characters in upper case
			word_list = get_words(lst, 'word_bank.txt') #gets list of words possible to make with these letters
			return render_template('wordcookies-output.html', title='Results', word_list=word_list)
		return render_template('wordcookies-input.html', title='Word Cookies', form=form)
	except Exception as e:
		print("ERROR: ", str(e))

if __name__ == "__main__":
    app.run()
