import os
import pymysql
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

# flask
app = Flask(__name__)

# 加载flask配置
app.config.root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config.from_pyfile('config.py')

# database
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)

# bootstrap
bootstrap = Bootstrap(app)

# flask-login
lm = LoginManager()
lm.init_app(app)
lm.session_protection = 'strong'
lm.login_view = 'login'

# 注册邮件组件
mail = Mail(app)

# 注册蓝图
from app.auth import auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# 自定义匿名用户注册
from app import views, models
lm.anonymous_user = models.AnonymousUser


# flask-manager
manager = Manager(app)

# flask-manager参数设置
# 第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app, db)

# manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db', MigrateCommand)