from flask import Flask, Blueprint, render_template, request, session
from random import randint
from db import *
import operator
from helpers import *
import nltk
import json

chat = Blueprint('chat', __name__)
	
@chat.route('/')
def index():
	if session.get('session_id') is None:
		session['session_id'] = str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))
		
	messageList = []
	results = message.query.filter_by(session_id=session['session_id']).order_by(message.id)
	for result in results:
		newItem = type('tmp', (object,), {})
		newItem.text = result.text
		newItem.time = result.time
		newItem.party = result.party
		if result.party is None:
			newItem.party = 1
			
		messageList.append(newItem)
		
	return render_template("index.html", messages = messageList)
	
@chat.route('/process_chat', methods=['POST'])
def process_chat():
	if session.get('session_id') is not None:
		insertMessage = message(request.form.get('message'), 1, session['session_id'])
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
		
		insertMessage = message(responseText, 0, session['session_id'])
		db.session.add(insertMessage)
		db.session.commit()
		
		return responseText
	else:
		return False
		
@chat.route('/process_response_slack', methods=['POST'])
def process_response_slack():
	inputMessage = request.form.get('text')
	
	#Figure out the subject node in the semantic graph
	subjectNode = determine_node(inputMessage)
	responseText = determine_response(inputMessage, subjectNode)
	
	insertMessage = message(inputMessage, 1, 0)
	db.session.add(insertMessage)
	db.session.commit()
	
	responseObj = json.dumps('{"response_type": "in_channel", "text": "' + responseText + '"}')
	
	return responseObj

def determine_node(inputMessage):
	inputList = clean_string(inputMessage).lower().split()
	posTag = nltk.pos_tag(inputList)
	
	nodeList = {}
	counter = 0
	for word in inputList:
		searchString = "%" + word + "%"
		results = training_chat.query.filter(training_chat.text.ilike(searchString))
		
		anyResults = False	
		for result in results:
			anyResults = True
			
			addAmount = 0
			if result.party == 0:
				addAmount += 1
			else:
				addAmount += 3
			
			resultCount = training_chat.query.filter_by(node_id = result.node_id).count()
			addAmount /= resultCount #Divide by the number of training chats pointing to that node
			
			#print(posTag[counter][0] + ' - ' + posTag[counter][1])
			if posTag[counter][1] == 'NN' or posTag[counter][1] == 'NNS' or posTag[counter][1] == 'NNP' or posTag[counter][1] == 'NNPS':
				addAmount *= 3
			elif posTag[counter][1] == 'JJ' or posTag[counter][1] == 'JJS' or posTag[counter][1] == 'JJR':
				addAmount *= 2
				
			if result.node_id in nodeList:
				nodeList[result.node_id] += addAmount
			else:
				nodeList[result.node_id] = addAmount
		
		counter += 1

	if anyResults:
		topNode = max(nodeList, key=nodeList.get)
		return topNode
	else:
		return 0

def determine_response(inputMessage, subjectNode):
	results = training_chat.query.all()
	for result in results:
		if clean_string(result.text).lower() == clean_string(inputMessage).lower():
			result2 = training_chat.query.order_by(training_chat.id).filter_by(chat_id=result.chat_id).filter(training_chat.id > result.id).first()
			return result2.text
	
	if subjectNode is not 0:
		results = training_chat.query.filter_by(node_id=subjectNode).order_by(training_chat.id)
		responseText = results[1].text
	else:
		responseText = "Sorry, I didn't understand that"
	
	return responseText
