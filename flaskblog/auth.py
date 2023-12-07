from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from .form import (LoginForm, RegistrationForm,
                PostForm, RequestResetForm, ResetPasswordForm)
from . import bcrypt, db, mail
from .models import User, Post
from flask_login import (login_required, login_user, logout_user, current_user)
from flask_mail import Message


auth = Blueprint('auth', __name__)

'''
   # check_username = User.query.filter_by(username=form.username.data.replace(" ", "")).first()
   # check_email = User.query.filter_by(email=form.email.data.casefold()).first()
   # if check_username:
   #    flash('This username is already exists.Please choose another!',category='danger')
   # elif check_email:
   #    flash('This email is already exists.Please choose another!',category='danger')
   # elif form.password.data != form.confirm_password.data:
   #    flash('Passwords does not match!',category='danger')
   # else:
   
   # from file import a
   # @auth.route('/db')
   # def base():
   #    for data in a:
   #       post = Post(title=data['title'],content=data['content'],user_id=data['user_id'])
   #       db.session.add(post)
   #    db.session.commit()
   #    return redirect(url_for('auth.login'))
'''


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        pwd_hss = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        new_user = User(username=form.username.data.replace(" ", ""),
                        email=form.email.data.casefold(), password=pwd_hss)
        db.session.add(new_user)
        db.session.commit()
        flash(
            "Your account has been created! You are now able to log in !",
            category='success',
        )
        return redirect(url_for('auth.login'))

    return render_template('register.html', title='Register', form=form, user=current_user)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        flash("Login Unsuccessful. Please check your Email and password",
            category='danger')
    return render_template('login.html', title='Login', form=form, user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/post/new', methods=['POST', 'GET'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        posts = Post(title=form.title.data,
                    content=form.content.data, user_id=current_user.id)
        db.session.add(posts)
        db.session.commit()
        flash('Your Post has been created!', 'success')
        return redirect(url_for('views.home'))
    return render_template('create_post.html', title='New Post', form=form, user=current_user, legend='New Post')


@auth.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, user=current_user)


@auth.route('/post/<int:post_id>/update', methods=['POST', 'GET'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been Updated", 'success')
        return redirect(url_for('auth.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, user=current_user, legend='Update Post')


@auth.route('/post/<int:post_id>/delete', methods=['POST', 'GET'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Your Post has been deleted", 'success')
        return redirect(url_for('views.home'))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='papaabdoulayendoye23@gmail.com',
                  recipients=['papaabdoulayepipo@gmail.com'])
    msg.body = f'''To Reset your Password Visit your following link:
{url_for('auth.reset_token',token=token,_external=True)}

If you did not make this request then simply ignore this email and no changes will be made. 
'''
    mail.send(msg)


@auth.route('/reset-password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email has been sent with instruction to reset your password.", 'info')
        return redirect(url_for('auth.login'))
    return render_template('reset_request.html', form=form, title='Reset Password')


@auth.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('auth.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        pwd_hss = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = pwd_hss
        db.session.commit()
        flash(
            "Your password has been updated! You are now able to log in !",
            category='success',
        )
        return redirect(url_for('auth.login'))

    return render_template('reset_token.html', form=form, title='Reset Password')
