from flask import render_template, flash, redirect, request
from app import app
from ftplib import FTP
from .forms import LoginForm

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Connection requested for "%s"' %
              (form.openid.data))
        if form.openid.data == 'localhost':
            ftp = FTP(form.openid.data)
            if ftp != 0:
                if ftp.login(form.user.data, form.passwd.data):
                    return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form)
    

@app.route('/index')

def index():
	user = {'nickname': 'FerPer'}  # fake user
	return render_template('index.html',
                           title='Home',
                           user=user)