from flask import render_template, redirect, g, url_for, flash
from flask_login import logout_user, login_user, login_required, current_user
from app import db
from app.auth import auth_blueprint
from app.form import LoginForm, RegistrationForm
from app.models import User


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # 已登录则返回首页
    if g.user is not None and g.user.is_authenticated:
        return redirect('/index')

    # POST接受表单数据
    form = LoginForm()
    # validate_on_submit 的作用是表单处理（包括验证）。如果验证不通过，也直接展示GET页面
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is None or user == '':
            flash('找不到该用户')
            return render_template('login.html', form=form)

        if user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # return redirect(request.args.get('next'))
            return redirect(url_for('index'))
        else:
            flash('账号名或密码错误')
            return render_template('login.html', form=form)

    # GET展示登录视图
    return render_template('login.html', form=form)


@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        token = user.generate_confirmation_token()
        user.send_email(user.email, 'Confirm Your Account', 'email/confirm', token=token)
        flash('验证邮件已发送，请登录邮箱以完成注册')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_blueprint.route('/confirm/<token>', methods=['GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('index'))
    if current_user.confirm_token(token):
        flash('You have confirmed your account. Thanks!')
        return redirect(url_for('index'))
    else:
        flash('The confirmation link is invalid or has expired.')
        return redirect(url_for('index'))
