from flask import render_template, flash, redirect
from app import app
from ftplib import FTP
from .forms import LoginForm


session = {'ftp': FTP, 'user': {'nickname': 'Anonymous'}}


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Connection requested for "%s"' %
              (form.openid.data))
        ftp = FTP(form.openid.data)
        session['ftp'] = ftp
        ftp.login(form.user.data, form.passwd.data)
        session['user'] = {'nickname': form.user.data}
        return redirect('/ftpserver')
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
    data = []
    data = ftp.nlst()
    return render_template('index.html',
                           title='Home',
                           user=user,
                           data=data)
