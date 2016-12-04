from db import *

def node_select_list():
	returnString = "<select name=\"node_list\" id=\"node_list_select\" class=\"form-control\">"
	
	results = semantic_graph_node.query.order_by(semantic_graph_node.title.asc())
	if not results:
		returnString += "<option value=\"\">No results found</option>"
	else:
		returnString += "<option value=\"\">Pick one</option>"
		for node in results:
			returnString += "<option value=\"" + str(node.id) + "\">" + node.title + "</option>"
		
	returnString += "</select>"
	
	return returnString

def clean_string(inputString):
	whitelist = set('abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ')
	outputString = ''.join(filter(whitelist.__contains__, inputString))
	
	return outputString

def clean_training_chats(inputList):
	chats = []
	for result in inputList:
		addResult = True
		for chat in chats:
			if chat.chat_id == result.chat_id:
				addResult = False
				break
		
		if addResult:
			chats.append(result)
	
	return chats
