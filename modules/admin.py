from flask import Flask, Blueprint, render_template, request, session
from db import *
from helpers import node_select_list

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
	if "del" in request.args:
		semantic_graph_node.query.filter_by(id=request.args["del"]).delete()
		db.session.commit()
		
	return render_template("graph.html", nodes = semantic_graph_node.query.all())

@admin.route('/graph', methods=['POST'])
def add_node():
	insertNode = semantic_graph_node(request.form.get('title'))
	db.session.add(insertNode)
	db.session.commit()
	
	return graph()

@admin.route('/node')
def view_node():
	nodeID = request.args['id']
	
	if "del" in request.args:
		semantic_graph_relationship.query.filter_by(id=request.args["del"]).delete()
		db.session.commit()
	
	nodeList = []
	
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
	
	return render_template("node.html", nodes = nodeList, node_id = nodeID)
	
@admin.route('/node', methods=['POST'])
def add_relationship_process():
	nodeID = request.args['id']
	insertRelationship = semantic_graph_relationship(nodeID, request.form.get('node_list'), request.form.get('relationship_1_to_2'), request.form.get('relationship_2_to_1'))
	db.session.add(insertRelationship)
	db.session.commit()
	
	return view_node()

@admin.route('/add_relationship')
def add_relationship_form():
	return render_template("add_relationship.html", node_id = request.args['id'], node_select_list = node_select_list())
