from flaskblog import Create_app,app
from flaskblog.models import Post
if __name__ == '__main__':
   app = Create_app()
   app.run(debug=True)
