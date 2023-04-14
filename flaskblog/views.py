import secrets
from flask import Blueprint, redirect, url_for, render_template, flash, request
from flask_login import current_user, login_required
from .form import UpdateAccountForm
from . import db
from . import UPLOAD_IMG
from .models import Post,User
from werkzeug.utils import secure_filename
import os
from PIL import Image

views = Blueprint('views', __name__)




@views.route('/')
@views.route('/home')
@login_required
def home():
   page = request.args.get('page',1,type=int)
   posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
   return render_template('home.html', posts=posts, title="Home", user=current_user)


@views.route('/about')
@login_required
def about():
   return render_template('about.html', user=current_user)



@views.route('/account', methods=['POST', 'GET'])
@login_required
def account():  # sourcery skip: remove-empty-nested-block
   form = UpdateAccountForm()
   if form.validate_on_submit():
      
      if form.picture.data:
         IMG_FILE = form.picture.data
         F = secure_filename(IMG_FILE.filename)
         FILE_PATH = os.path.join(UPLOAD_IMG, F)
         img = Image.open(IMG_FILE)
         OUTPUT_SIZE = (125,125)
         img.thumbnail(OUTPUT_SIZE)
         img.save(FILE_PATH)
         current_user.image_file = F
         db.session.commit()
      
      current_user.username = form.username.data.replace(' ', '')
      current_user.email = form.email.data.casefold()
      db.session.commit()
      flash('Your account has been updated!', category='success')
      return redirect(url_for('views.account'))
   form.username.data = current_user.username
   form.email.data = current_user.email
   image_file = url_for('static', filename='img/' + current_user.image_file)
   return render_template('account.html', tittle="Account",
                              user=current_user, image_file=image_file, form=form)




@views.route('/user/<string:username>')
def user_posts(username):
   page = request.args.get('page',1,type=int)
   user = User.query.filter_by(username=username).first_or_404()
   posts = Post.query.filter_by(author=user)\
            .order_by(Post.date_posted.desc())\
            .paginate(page=page,per_page=5)
   return render_template('user_post.html', posts=posts,user=user)




