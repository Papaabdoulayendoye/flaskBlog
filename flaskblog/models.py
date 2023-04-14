from . import db, app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import URLSafeSerializer


class User(db.Model, UserMixin):
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(20), unique=True, nullable=False)
   email = db.Column(db.String(120), unique=True, nullable=False)
   password = db.Column(db.String(60), nullable=False)
   image_file = db.Column(
      db.String(120), nullable=False, default="default.jpg")
   posts = db.relationship('Post', backref="author", lazy=True)

   def get_reset_token(self, expires_sec=1800):
      s = URLSafeSerializer(app.config['SECRET_KEY'], salt='reset_password')
      return s.dumps({'user_id': self.id}, salt='reset_password')

   @staticmethod
   def verify_reset_token(token):
      s = URLSafeSerializer(app.config['SECRET_KEY'], salt='reset_password')
      try:
         user_id = s.loads(token, salt='reset_password')['user_id']
      except Exception:
         return None
      return User.query.get(user_id)


class Post(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False)
   date_posted = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.utcnow)
   content = db.Column(db.Text, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

   # def __repr__(self):
   #    return f"User('{self.title}'|||'{self.date_posted}'|||'{self.content}'|||'{self.user_id}')"
