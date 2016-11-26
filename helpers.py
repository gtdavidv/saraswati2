from db import *

def node_select_list():
	returnString = "<select name=\"node_list\">"
	
	results = semantic_graph_node.query.order_by(semantic_graph_node.title.asc())
	if not results:
		returnString += "<option value=\"\">No results found</option>"
	else:
		returnString += "<option value=\"\">Pick one</option>"
		for node in results:
			returnString += "<option value=\"" + str(node.id) + "\">" + node.title + "</option>"
		
	returnString += "</select>"
	
	return returnString
