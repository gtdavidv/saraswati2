from flask import Flask, Blueprint, render_template, request, session
from db import *
import operator
from helpers import *

chat = Blueprint('chat', __name__)
	
@chat.route('/process_chat', methods=['POST'])
def process_chat():
	if session.get('session_id') is not None:
		insertMessage = message(request.form.get('message'), session['session_id'])
		db.session.add(insertMessage)
		db.session.commit()
		
	return 'ok'

@chat.route('/process_response', methods=['POST'])
def process_response():
	if session.get('session_id') is not None:
		inputMessage = request.form.get('message')
		
		#Figure out the subject node in the semantic graph
		subjectNode = determine_node(inputMessage)
		responseText = determine_response(inputMessage, subjectNode)
		
		insertMessage = message(responseText, session['session_id'])
		db.session.add(insertMessage)
		db.session.commit()
		
		return responseText
	else:
		return False

def determine_node(inputMessage):
	inputList = inputMessage.split()
	
	nodeList = {}
	for word in inputList:
		searchString = "%" + word + "%"
		results = training_chat.query.filter(training_chat.text.like(searchString))
		
		anyResults = False	
		for result in results:
			anyResults = True
			if result.node_id in nodeList:
				nodeList[result.node_id] += 1
			else:
				nodeList[result.node_id] = 1

	if anyResults:
		topNode = max(nodeList, key=nodeList.get)
		return topNode
	else:
		return 0

def determine_response(inputMessage, subjectNode):
	results = training_chat.query.all()
	for result in results:
		if clean_string(result.text).lower() == clean_string(inputMessage).lower():
			print('YES')
			result2 = training_chat.query.order_by(training_chat.id).filter_by(chat_id=result.chat_id).filter(training_chat.id > result.id).first()
			return result2.text
		else:
			print(clean_string(result.text) + ' is not ' + clean_string(inputMessage))
	
	if subjectNode is not 0:
		results = training_chat.query.filter_by(node_id=subjectNode).order_by(training_chat.id)
		responseText = results[1].text
	else:
		responseText = "Sorry, I didn't understand that"
	
	return responseText
