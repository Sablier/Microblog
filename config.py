import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'go-fuck-yourself'

# Flask-SQLAlchemy 配置
# SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@192.168.119.132:3306/SablierBlog'
SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1:3306/SablierBlog'
# SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ECHO = True

# SQLAlchemy-migrate 配置
SQLALCHEMY_MIGRATE_REPO = os.path.join(BASEDIR, 'db_repository')

# Flask-Mail 配置
MAIL_SERVER = 'smtp.163.com'  # 发邮件主机
MAIL_PORT = 465  # 发邮件端口
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'Mrsablier@163.com'  # 授权的邮箱
MAIL_PASSWORD = 'Sablieradmin183'  # 邮箱授权时获得的密码，非注册登录密码
MAIL_SUBJECT_PREFIX = 'SablierBlog'
MAIL_DEFAULT_SENDER = 'SablierBlog<MrSablier@163.com>'
