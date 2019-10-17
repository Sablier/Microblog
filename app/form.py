from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    """登录表单"""
    email = wtforms.StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = wtforms.PasswordField('Password', validators=[DataRequired()])
    remember_me = wtforms.BooleanField('remember_me', default=False)
    submit = wtforms.SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """注册表单"""
    email = wtforms.StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = wtforms.StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp(r'^[A-Za-z][A-Za-z0-9_.]*$', message='用户名格式错误，仅可使用字母数字下划线和点')])
    password = wtforms.PasswordField('Password', validators=[DataRequired()])
    password2 = wtforms.PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password', message='两次密码不一致')])
    submit = wtforms.SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email地址已存在')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在')
