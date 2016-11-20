from flask import Flask, Blueprint, render_template, request, session
from db import *

chat = Blueprint('chat', __name__)
	
@chat.route('/process_chat', methods=['POST'])
def process_chat():
	if session.get('session_id') is not None:
		insertMessage = message(request.form.get('message'), session['session_id'])
		db.session.add(insertMessage)
		db.session.commit()
		
	return 'ok'
