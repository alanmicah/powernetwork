# import json
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

# # create the extension
# db = SQLAlchemy()
# # create the app
# app = Flask(__name__)
# # configure the SQLite database, relative to the app instance folder
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
# # initialize the app with the extension
# db.init_app(app)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/alanmicah'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'FALSE'
db = SQLAlchemy(app)

@app.route("/")
def index():
   return render_template("index.html")

if __name__=='__main__':
   app.debug=True
   app.run(host='0.0.0.0')
   # session_options={"autoflush": False}

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
    

#     def __repr__(self):
#         return '<User %r>' % self.username

# if __name__=='__main__':
#    app.debug=True
# app.run()

# @app.route('/')
# def hello_world():
#    return 'Hello Tutorialspoint'

# @app.route('/getreports')
# async def fetch_das_db():
#    try_live_reports()
#    # response = DASDBData().get_all()
#    # logger.info("---ASYNCRONOUS----")
#    # return (json.dumps(await response))


# @app.route('/')
# def index(): pass

# @app.route('/login')
# def login(): pass

# @app.route('/user/')
# def profile(username): pass

# with app.test_request_context():
#     print( url_for('index'))
#     print( url_for('index', _external=True))
#     print( url_for('login'))
#     print( url_for('login', next='/'))
#     print( url_for('profile', username='Tutorials Point'))
