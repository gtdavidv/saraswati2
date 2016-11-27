function check_add_training_chat(){
	var node = document.getElementById('node_list_select').value;
	var message = document.getElementById('message').value;
	
	var valid = true;
	
	if (node == ''){
		valid = false;
		document.getElementById('node_list_select').style.backgroundColor = '#FFCCCC';
	}
	if (message == ''){
		valid = false;
		document.getElementById('message').style.backgroundColor = '#FFCCCC';
	}
	
	return valid;
}
