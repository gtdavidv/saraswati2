from flask import Flask, render_template, request, session, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from time import time
from random import randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'false'
Bootstrap(app)

"""
Database setup
"""

db = SQLAlchemy(app)

"""
" The main chat model - where the user's submissions and the bot's response are stored
"""
class message(db.Model):
	id = db.Column('message_id', db.Integer, primary_key = True)
	text = db.Column(db.Text)
	time = db.Column(db.Integer, default=time)
	session_id = db.Column(db.Integer)

	def __init__(self, text, session_id):
		self.text = text
		self.session_id = session_id

"""
" Training chats model
"""
class training_chat(db.Model):
	id = db.Column('message_id', db.Integer, primary_key = True)
	chat_id = db.Column(db.Integer)
	party = db.Column(db.SmallInteger)
	text = db.Column(db.Text)
	node_id = db.Column(db.Integer)

	def __init__(self, chat_id, party, text, node_id):
		self.chat_id = chat_id
		self.party = party
		self.text = text
		self.node_id = node_id

"""
" Model for the nodes of the semantic graph
"""
class semantic_graph_node(db.Model):
	id = db.Column('node_id', db.Integer, primary_key = True)
	title = db.Column(db.String(255))

	def __init__(self, title):
		self.title = title

"""
" Model for the relationships that connect the nodes of the semantic graph
"""
class semantic_graph_relationship(db.Model):
	id = db.Column('relationship_id', db.Integer, primary_key = True)
	node_id_1 = db.Column(db.Integer)
	node_id_2 = db.Column(db.Integer)
	relationship_1_to_2 = db.Column(db.String(255))
	relationship_2_to_1 = db.Column(db.String(255))

	def __init__(self, node_id_1, node_id_2, relationship_1_to_2, relationship_2_to_1):
		self.node_id_1 = node_id_1
		self.node_id_2 = node_id_2
		self.relationship_1_to_2 = relationship_1_to_2
		self.relationship_2_to_1 = relationship_2_to_1
	   
db.create_all()

"""
Routes & Controllers
"""

@app.route('/')
def index():
	if session.get('session_id') is None:
		session['session_id'] = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))
		
	return render_template("index.html", messages = message.query.filter_by(session_id=session['session_id']))
	
@app.route('/process_chat', methods=['POST'])
def process_chat():
	if session.get('session_id') is not None:
		insertMessage = message(request.form.get('message'), session['session_id'])
		db.session.add(insertMessage)
		db.session.commit()
		
	return 'ok'
	

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/faq')
def faq():
	return render_template("faq.html")

@app.route('/contact')
def contact():
	return render_template("contact.html")

@app.route('/admin')
def admin():
	return render_template("admin.html")

@app.route('/training_chats')
def training_chats():
	return render_template("training_chats.html", chats = training_chat.query.distinct(training_chat.chat_id))
	
@app.route('/training_chat')
def render_training_chat():
	return render_template("training_chat.html")

@app.route('/training_chat', methods=['POST'])
def add_training_chat():
	if request.form.get('chat_id') is None:
		lastRecord = training_chat.query.order_by(training_chat.chat_id.desc()).first()
		if lastRecord is not None:
			chat_id = lastRecord.chat_id + 1
		else:
			chat_id = 1
	else:
		chat_id = request.form.get('chat_id')
		
	insertMessage = training_chat(chat_id, request.form.get('party'), request.form.get('message'), request.form.get('node_id'))
	db.session.add(insertMessage)
	db.session.commit()
	
	return str(chat_id)
	
@app.route('/graph')
def graph():
	return render_template("graph.html")
	
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' #Needed for sessions apparently? Should be randomized?
app.run('0.0.0.0', 8080)
