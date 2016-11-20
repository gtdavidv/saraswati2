from flask import Flask, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from random import randint
from db import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
Bootstrap(app)

db.init_app(app)

from modules.basic import basic
app.register_blueprint(basic)
from modules.admin import *
app.register_blueprint(admin)
from modules.chat import *
app.register_blueprint(chat)
	
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #Needed for sessions apparently? Should be randomized?
app.run('0.0.0.0', 8080)
