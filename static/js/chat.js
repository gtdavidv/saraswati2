///////////////
// Autoselect the chat box
///////////////


///////////////
// Add listener for enter key when the chat box is selected (treat like submit)
///////////////
document.getElementById('chat-input').onkeyup = function(e) {
   var key = e.keyCode ? e.keyCode : e.which;

   if (key == 13) {
	   sendChat();
   }
}

///////////////
// Handles when the user submits the text in the chat bot
///////////////
sendChat = function(){
	//Send call to add to the database
	var oReq = new XMLHttpRequest();
	oReq.addEventListener("load", transferComplete);
	oReq.addEventListener("error", transferFailed);
	oReq.addEventListener("abort", transferCanceled);
	oReq.open("POST", 'process_chat', true);
	oReq.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	oReq.send("message=" + document.getElementById('chat-input').value);
	
	//Add to the screen
	var timestamp = new Date();
	addMessageToScreen(document.getElementById('chat-input').value, 'You', timestamp.getTime()/1000);
	document.getElementById('chat-messages').scrollTop = document.getElementById('chat-messages').scrollHeight;
	document.getElementById('chat-input').value = '';
}

///////////////
// Transfer response handlers
///////////////
transferComplete = function(){ console.log('Transfer complete'); }
transferFailed = function(){ console.log('Transfer failed'); }
transferCanceled = function(){ console.log('Transfer canceled'); }

///////////////
// Inserts a new chat bubble
///////////////
addMessageToScreen = function(message, agent, time){
	var parentDiv = document.createElement('div');
	parentDiv.className = 'chat-bubble-parent';
	var timestampDiv = document.createElement('div');
	timestampDiv.className = 'chat-bubble-timestamp pull-right';
	var chatDiv = document.createElement('div');
	chatDiv.className = 'chat-bubble pull-right';
	
	var date = new Date(time*1000);
	var hours = date.getHours();
	var minutes = "0" + date.getMinutes();
	var seconds = "0" + date.getSeconds();
	var displayTime = hours + ':' + minutes.substr(-2) + ':' + seconds.substr(-2);
	
	chatDiv.innerHTML = message;
	timestampDiv.innerHTML = displayTime
	
	parentDiv.appendChild(timestampDiv);
	parentDiv.appendChild(chatDiv);
	document.getElementById('chat-messages').appendChild(parentDiv);
}
