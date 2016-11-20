from flask import Flask, Blueprint, render_template, request, session
from db import *

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_page():
	return render_template("admin.html")

@admin.route('/training_chats')
def training_chats():
	return render_template("training_chats.html", chats = training_chat.query.distinct(training_chat.chat_id))
	
@admin.route('/training_chat')
def render_training_chat():
	return render_template("training_chat.html")

@admin.route('/training_chat', methods=['POST'])
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
	
@admin.route('/graph')
def graph():
	return render_template("graph.html")
