from flask_sqlalchemy import SQLAlchemy
from time import time

db = SQLAlchemy()

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

#db.create_all()
