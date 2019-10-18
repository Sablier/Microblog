from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from flask_login._compat import text_type
from app import db, lm, mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_mail import Message
from flask import current_app, render_template
from email.mime.multipart import MIMEMultipart
import smtplib


class AnonymousUser(AnonymousUserMixin):
    """主要用户主页在没有登录状态下调用user的各种属性"""

    @property
    def name(self):
        return ''

    @property
    def confirmed(self):
        return False


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)  # 邮件验证

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % (self.nickname)

    # flask-login要求的属性和方法
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    # flask_login的回调函数(定义flask_login给系统的返回值，这里flask_login将返回一个user对象)
    @lm.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # password属性
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')  # password属性不可以直接读取

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 邮件验证
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def send_email(self, to, subject, template, **kwargs):
        msg = Message(subject=current_app.config['MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                      sender=current_app.config['MAIL_DEFAULT_SENDER'], recipients=[to])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)

        # msgRoot = MIMEMultipart('related')
        # msgRoot['From'] = current_app.config['MAIL_SENDER']
        # msgRoot['To'] = to
        # msgRoot['Subject'] = subject
        #
        # smtp = smtplib.SMTP_SSL(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT'])
        # smtp.set_debuglevel(1)
        # smtp.helo(current_app.config['MAIL_SERVER'])
        # smtp.ehlo(current_app.config['MAIL_SERVER'])
        # smtp.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
        # smtp.sendmail(current_app.config['MAIL_USERNAME'], to, msgRoot.as_string())
        mail.send(msg)

    def confirm_token(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.commit()
        return True


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)



