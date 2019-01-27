from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm, GetLetters

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        abc = str(form.username.data)
        print (form.username.data)
        return abc
    return render_template('login.html', title='Sign In', form=form)


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
                print (item)
        return sort_lst	
	
	
	
@app.route('/wordcookies', methods=['GET', 'POST'])
def wordcookies():
    form = GetLetters()
    if form.validate_on_submit():
        lst = list()
        n = 0
        for letter in form.letters.data:
            lst.append(letter.upper()) #makes list of characters in upper case
        word_list = get_words(lst, 'word_bank.txt') #gets list of words possible to make with these letters
        return render_template('wordcookies-output.html', title='Results', word_list=word_list)
    return render_template('wordcookies-input.html', title='WordCookies', form=form)
