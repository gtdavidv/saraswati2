from flask import Flask, Blueprint, render_template, request, session
from random import randint
from db import *
import operator
from helpers import *
import nltk

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

def determine_node(inputMessage):
	inputList = clean_string(inputMessage).lower().split()
	posTag = nltk.pos_tag(inputList)
	
	nodeList = {}
	counter = 0
	for word in inputList:
		searchString = "%" + word + "%"
		results = training_chat.query.filter(training_chat.text.ilike(searchString))
		resultCount = training_chat.query.filter(training_chat.text.ilike(searchString)).count()
		
		anyResults = False	
		for result in results:
			anyResults = True
			
			addAmount = 0
			if result.party == 0:
				addAmount += 1
			else:
				addAmount += 3
			addAmount /= resultCount
			
			if posTag[counter][1] == 'NN' or posTag[counter][1] == 'NNS' or posTag[counter][1] == 'NNP' or posTag[counter][1] == 'NNPS':
				addAmount *= 3
				#print(posTag[counter][0] + ' - ' + posTag[counter][1])
				
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
