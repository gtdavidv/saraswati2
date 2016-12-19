from flask import Flask, Blueprint, render_template, request, session, redirect
from db import *
from helpers import node_select_list, clean_training_chats

admin = Blueprint('admin', __name__)

@admin.route('/admin')
def admin_page():
	return render_template("admin.html")

@admin.route('/training_chats')
def training_chats():
	results = training_chat.query.order_by(training_chat.chat_id).all()
	chats = clean_training_chats(results)
			
	return render_template("training_chats.html", chats = chats)
	
@admin.route('/training_chat')
def render_training_chat():
	if "id" in request.args:
		nodeID = None
		chatID = request.args["id"]
		results = training_chat.query.filter_by(chat_id=chatID)
		if not results:
			return render_template("error.html", error_message = "Database error")
		else:
			if "del" in request.args:
				training_chat.query.filter_by(id=request.args["del"]).delete()
				db.session.commit()
				
			training_chats = []
			for result in results:
				nodeID = result.node_id
				newItem = type('tmp', (object,), {})
				
				graphNode = semantic_graph_node.query.filter_by(id=result.node_id).first()
				if not graphNode:
					#return render_template("error.html", error_message="Database error: missing node")
					newItem.node_name = 'n/a'
				else:
					newItem.node_name = graphNode.title
				
				newItem.party = result.party
				newItem.text = result.text
				newItem.node_id = result.node_id
				
				newItem.id = result.id
				training_chats.append(newItem)
	else:
		training_chats = []
		chatID = 0
		nodeID = 0
		
	return render_template("training_chat.html", node_select_list = node_select_list(nodeID), chats = training_chats, chat_id = chatID)

@admin.route('/training_chat', methods=['POST'])
def add_training_chat():
	if "id" not in request.args:
		lastRecord = training_chat.query.order_by(training_chat.chat_id.desc()).first()
		if lastRecord is not None:
			chat_id = lastRecord.chat_id + 1
		else:
			chat_id = 1
	else:
		chat_id = request.args["id"]
		
	insertMessage = training_chat(chat_id, request.form.get('party'), request.form.get('message'), request.form.get('node_list'))
	db.session.add(insertMessage)
	db.session.commit()
	
	return redirect("training_chat?id=" + str(chat_id))
	
	#return render_training_chat()
	
@admin.route('/graph', methods=['POST'])
def add_node():
	insertNode = semantic_graph_node(request.values.get('title'))
	db.session.add(insertNode)
	db.session.commit()
	
	return graph()

@admin.route('/graph')
def graph():
	if "del" in request.args and "title" not in request.values:
		delNode = semantic_graph_node.query.filter_by(id=request.args["del"]).first()
		db.session.delete(delNode)
		db.session.commit()
		
	return render_template("graph.html", nodes = semantic_graph_node.query.all())

@admin.route('/node', methods=['POST'])
def add_relationship_process():
	nodeID = request.args['id']
	insertRelationship = semantic_graph_relationship(nodeID, request.form.get('node_list'), request.form.get('relationship_1_to_2'), request.form.get('relationship_2_to_1'))
	db.session.add(insertRelationship)
	db.session.commit()
	
	return view_node()

@admin.route('/node')
def view_node():
	nodeID = request.args['id']
	thisNode = semantic_graph_node.query.filter_by(id=nodeID).first()
	if not thisNode:
		return render_template("error.html", error_message = "Database error")
	else:
		nodeName = thisNode.title
	
	if "del" in request.args:
		semantic_graph_relationship.query.filter_by(id=request.args["del"]).delete()
		db.session.commit()
	
	nodeList = []
	
	#Need to get all of the relationships (node_id_1 and node_id_2
	queryList = semantic_graph_relationship.query.filter_by(node_id_1 = nodeID)
	for result in queryList:
		newItem = type('tmp', (object,), {}) #Hacky way to make newItem a generic object
		newItem.relationship_id = result.id
		newItem.relationship = result.relationship_2_to_1 #Show the relationship of node2 to node1
		newItem.other_node_id = result.node_id_2
		
		titleQuery = semantic_graph_node.query.filter_by(id = result.node_id_2).first()
		newItem.nodeTitle = titleQuery.title
		nodeList.append(newItem)
	
	queryList2 = semantic_graph_relationship.query.filter_by(node_id_2 = nodeID)
	for result in queryList2:
		newItem = type('tmp', (object,), {}) #Hacky way to make newItem a generic object
		newItem.relationship_id = result.id
		newItem.relationship = result.relationship_1_to_2 #Show the relationship of node1 to node2
		newItem.other_node_id = result.node_id_1
		
		titleQuery = semantic_graph_node.query.filter_by(id = result.node_id_1).first()
		newItem.nodeTitle = titleQuery.title
		nodeList.append(newItem)
		
	results = training_chat.query.order_by(training_chat.chat_id).filter_by(node_id = nodeID)
	chats = clean_training_chats(results)
	
	return render_template("node.html", nodes = nodeList, node_id = nodeID, node_name = nodeName, chats = chats)

@admin.route('/add_relationship')
def add_relationship_form():
	nodeID = request.args['id']
	
	thisNode = semantic_graph_node.query.filter_by(id=nodeID).first()
	if not thisNode:
		return render_template("error.html", error_message = "Database error")
	else:
		nodeName = thisNode.title
		
	return render_template("add_relationship.html", node_id = nodeID, node_select_list = node_select_list(), node_name = nodeName)
	
@admin.route('/chat_history')
def chat_history():
	messageList = []
	results = message.query.order_by(message.id)
	for result in results:
		newItem = type('tmp', (object,), {})
		newItem.text = result.text
		newItem.time = result.time
		newItem.party = result.party
		if result.party is None:
			newItem.party = 1
			
		messageList.append(newItem)
		
	return render_template("chat_history.html", messages = messageList)
