from flask import render_template, flash, redirect
from app import app
from ftplib import FTP
from .forms import LoginForm
import socket


session = {'ftp': FTP, 'user': {'nickname': 'Anonymous'}}


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Connection requested for "%s"' %
              (form.openid.data))
        try:
            host = socket.gethostbyname(form.openid.data)
            socket.create_connection((host, 21), 2)
            ftp = FTP(form.openid.data)
            session['ftp'] = ftp
            try:
                ftp.login(form.user.data, form.passwd.data)
                session['user'] = {'nickname': form.user.data}
                return redirect('/ftpserver')
            except Exception:
                flash('Wrong user or password')
        except Exception:
            flash('Not a FTP server')
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/ftpserver')
def ftpserver():
    user = session['user']  # fake user
    ftp = session['ftp']
    data = {'name': [], 'permissions': []}
    permission = []
    ftp.dir(permission.append)
    data['name'] = ftp.nlst()
    for p in permission:
        p, empty = p.split(' ', 1)
        data['permissions'].append(p)
    return render_template('index.html',
                           title='Home',
                           user=user,
                           data=data)
