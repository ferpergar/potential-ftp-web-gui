from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    user = StringField('user', validators=[DataRequired()])
    passwd = PasswordField('passwd', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)