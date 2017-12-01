from flask import render_template, flash, redirect, request, url_for, session
from app import app
from ftplib import FTP
from .forms import LoginForm

session = {'ftp': FTP, 'user': {'nickname': 'FerPer'}}

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])

def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Connection requested for "%s"' %
              (form.openid.data))
        if form.openid.data == 'localhost':
            ftp = FTP(form.openid.data)
            session['ftp'] = ftp
            if ftp != 0:
                if ftp.login(form.user.data, form.passwd.data):
                    session['user'] = {'nickname': form.user.data}
                    return redirect('/ftpserver')
                    #return redirect('/index')
    return render_template('login.html', 
                           title='Sign In',
                           form=form)
    

@app.route('/index')

def index():
	user = {'nickname': 'FerPer'}  # fake user
	return render_template('index.html',
                           title='Home',
                           user=user)

@app.route('/ftpserver')

def ftpserver():
  user = session['user']  # fake user
  ftp = session['ftp']
  ftp.dir()
  return render_template('index.html',
                           title='Home',
                           user=user)