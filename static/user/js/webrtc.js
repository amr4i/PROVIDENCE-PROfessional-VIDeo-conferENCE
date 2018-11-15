var localVideo;
var localStream;
var remoteVideo = {};
var remoteVideo2;
var peerConnection = {};
var isRemoteSet = {};
var streamIdToVideoElement = {};
var username;
var serverConnection;
var roomId = -1;
var streamsRecieved = 0;

var peerConnectionConfig = {
	'iceServers': [
		{'urls': 'stun:stun.stunprotocol.org:3478'},
		{'urls': 'stun:stun.l.google.com:19302'},
	]
};


function getUserMediaSuccess(stream) {
	localStream = stream;
	localVideo.srcObject = stream;
}


function gotMessageFromServer(signal) {
	// if(!peerConnection) start(false);

	// console.log(message);
	// console.log('************');
	// console.log(message.data);
	// var signal = JSON.parse(message);
	// var signal = message;
	// console.log(signal);
	console.log("Got Message");
	console.log(signal);

	// Ignore messages from ourself
	if(signal.uuid == username) return;
	// if(signal.uuid == uuid) return;
	// console.log(signal);

	if(signal.rid != roomId)
		return;

	// console.log(signal);

	// if(signal.sdp) {
	// 	peerConnection.setRemoteDescription(new RTCSessionDescription(signal.sdp)).then(function() {
	// 	// Only create answers in response to offers
	// 	if(signal.sdp.type == 'offer') {
	// 		peerConnection.createAnswer().then(createdDescription).catch(errorHandler);
	// 	}
 //    }).catch(errorHandler);
	// } else if(signal.ice) {
	// 	peerConnection.addIceCandidate(new RTCIceCandidate(signal.ice)).catch(errorHandler);
	// }

	if(isRemoteSet[signal.uuid] == false)
		return;

	if(signal.ice) {
		peerConnection[signal.uuid].addIceCandidate(new RTCIceCandidate(signal.ice)).catch(errorHandler);
	}
}



function createdDescription(description) {
	console.log('got description');

	peerConnection.setLocalDescription(description).then(function() {
		// serverConnection.send(JSON.stringify({'sdp': peerConnection.localDescription, 'uuid': uuid}));
		serverConnection.emit('sdp description', {'sdp': peerConnection.localDescription, 'uuid': username, 'rid': roomId});
	}).catch(errorHandler);
}

function gotRemoteStream(event) {
	console.log('got remote stream');
	
	// remoteVideo[streamsRunning] = document.getElementById("remoteVideo"+streamsRunning.toString());

	var streamId = event.streams[0].id;
	var remoteVideoAdded = document.createElement("VIDEO");
	remoteVideoAdded.id = "remoteVideo_"+streamId;
	remoteVideoAdded.style.width = "40%";
	remoteVideoAdded.autoplay = true;	
	console.log(event);
	remoteVideoAdded.srcObject = event.streams[0];
	
	// To handle asynchronicity of parallel threads
	// Else, each stream will get added multiple times due to multiple tracks.
	if(streamsRecieved++%2 == 0){
		document.getElementById('videoRoom').appendChild(remoteVideoAdded);
	}
}

// function gotRemoteStream(event) {
// 	console.log('got remote stream');
// 	console.log(event)
// 	remoteVideo.srcObject = event.streams[0];
// }

function start(isCaller) {
	// if(!isCaller){
	// 	console.log('aage kyon nahi bad raha');
	// }
	peerConnection = new RTCPeerConnection(peerConnectionConfig);
	peerConnection.onicecandidate = gotIceCandidate;
	peerConnection.ontrack = gotRemoteStream;
	peerConnection.addStream(localStream);

	if(isCaller) {
		peerConnection.createOffer().then(createdDescription).catch(errorHandler);
		// serverConnection.emit('create room', {'uuid': username});
	}
}


function endConnection(signal) {
	
	if(signal.rid != roomId) return;

	console.log("Ending Connection with ");
	console.log(signal.uuid);

	var streamId = peerConnection[signal.uuid].getRemoteStreams()[0].id;
	peerConnection[signal.uuid].onicecandidate = null;
	peerConnection[signal.uuid].ontrack = null
	
	// how to get which remote Video to which uuid? 
	// if (remoteVideo[].srcObject) {
 //      remoteVideo[].srcObject.getTracks().forEach(track => track.stop());
 //    }
 //    remoteVideo[].src = null;
    peerConnection[signal.uuid].close();
    delete peerConnection[signal.uuid];

    var videoElement = document.getElementById("remoteVideo_"+streamId);
    videoElement.parentNode.removeChild(videoElement);

    //shift all other remoteVideo elements after it
    // to cover up the blank space 

	// delete peerConnection[signal.uuid];	

}

////////////////////////////////////////////////////////////////////////////////////

function gotIceCandidate(event) {
	// console.log('in gotIceCandidate');
	if(event.candidate != null) {
		// console.log('in gotIceCandidate if');
		// serverConnection.send(JSON.stringify({'ice': event.candidate, 'uuid': uuid}));
		// serverConnection.emit('ice candidate', {'ice': event.candidate, 'uuid': uuid});
		serverConnection.emit('ice candidate', {'ice': event.candidate, 'uuid': username, 'rid': roomId});
	}
}

function addIce(signal) {
	// Ignore messages from ourself
	if(signal.uuid == username) return;

	if(signal.rid != roomId) return;

	console.log("Add ICE");
	console.log(signal);

	if(isRemoteSet[signal.uuid] == false)

		return;

	if(signal.ice) {
		console.log('Adding Candidate');
		peerConnection[signal.uuid].addIceCandidate(new RTCIceCandidate(signal.ice)).catch(errorHandler);
	}
}



function setRemoteDesc(signal){
	if(signal.new_user != username) return;

	if(signal.rid != roomId)
		return;

	console.log('In setRemoteDesc');
	console.log(signal);

	if(peerConnection.hasOwnProperty(signal.uuid) == false){
		peerConnection[signal.uuid] = new RTCPeerConnection(peerConnectionConfig);
		peerConnection[signal.uuid].onicecandidate = gotIceCandidate;
		peerConnection[signal.uuid].ontrack = gotRemoteStream;
		peerConnection[signal.uuid].addStream(localStream);
	}

	peerConnection[signal.uuid].setRemoteDescription(new RTCSessionDescription(signal.sdp)).then(function() {
		// Only create answers in response to offers
		isRemoteSet[signal.uuid] = true;
		if(signal.sdp.type == 'offer') {
			peerConnection[signal.uuid].createAnswer().then(function(description){
				console.log('In creating Answer');

				peerConnection[signal.uuid].setLocalDescription(description).then(function() {
					// serverConnection.send(JSON.stringify({'sdp': peerConnection.localDescription, 'uuid': uuid}));
					serverConnection.emit('sdp description', {'sdp': peerConnection[signal.uuid].localDescription,
																'uuid': username,
																'rid': roomId,
																'new_user': signal.uuid
															});
				}).catch(errorHandler);
			}).catch(errorHandler);
		}
	}).catch(errorHandler);
}


function restoreStateInRoom(signal) {
	document.getElementById("createRoomButton").hidden = true;
	document.getElementById("joinRoomButton").hidden = true;
	document.getElementById("leaveRoomButton").hidden = false;
	document.getElementById("createRoomButton").disabled = true;
	document.getElementById("joinRoomButton").disabled = true;
	document.getElementById("leaveRoomButton").disabled = false;
	document.getElementById("joinRoomId").hidden = true;
}


function restoreStateNotInRoom(signal) {
	document.getElementById("createRoomButton").hidden = false;
	document.getElementById("joinRoomButton").hidden = false;
	document.getElementById("leaveRoomButton").hidden = true;
	document.getElementById("createRoomButton").disabled = false;
	document.getElementById("joinRoomButton").disabled = false;
	document.getElementById("leaveRoomButton").disabled = true;
	document.getElementById("joinRoomId").hidden = false;
	document.getElementById("joinRoomId").value = "";
	document.getElementById("roomId").innerHTML = "";
	if(signal.type == "alert"){
		alert(signal.msg);
	}
}


function leaveRoom(event){
	console.log("Leaving Room");
	restoreStateNotInRoom({"type":"onLeave"});

	Object.keys(peerConnection).forEach(function(peerId) {
		var jsonSignal = {'uuid': peerId, 'rid': roomId};
		endConnection(jsonSignal);
	});

	serverConnection.emit('leave room', {'uuid': username, 'rid':roomId});
}

function createRoom(event){
	console.log("Create Room");
	restoreStateInRoom({"type":"onCreate"}); 

	serverConnection.emit('create room', {'uuid': username});
}


function joinRoom(event){
	var x = document.getElementById('joinRoomId');
	roomId = x.value;
	console.log("Join Room " + roomId);
	var p = document.getElementById('roomId');
	p.innerHTML = roomId;
	restoreStateInRoom({"type":"onJoin"});

	serverConnection.emit('join', {'uuid': username, 'rid': roomId});
}


function gotRoomId(message){
	var p = document.getElementById('roomId');
	console.log("Got Room Id ");
	console.log(message);
	p.innerHTML = message.data;
	roomId = message.data;
	// start(true);

	// console.log(message);
}


function createNewOffer(signal) {
	if (username == signal.new_user)
		return

	console.log('in createNewOffer');
	console.log(signal);

	peerConnection[signal.new_user] = new RTCPeerConnection(peerConnectionConfig);
	peerConnection[signal.new_user].onicecandidate = gotIceCandidate;
	peerConnection[signal.new_user].ontrack = gotRemoteStream;
	peerConnection[signal.new_user].addStream(localStream);

	peerConnection[signal.new_user].createOffer().then(function(description) {
		peerConnection[signal.new_user].setLocalDescription(description).then(function() {
			// serverConnection.send(JSON.stringify({'sdp': peerConnection.localDescription, 'uuid': uuid}));
			serverConnection.emit('sdp description', {'sdp': peerConnection[signal.new_user].localDescription,
														'uuid': username,
														'rid': roomId,
														'new_user': signal.new_user});
		}).catch(errorHandler);
	}).catch(errorHandler);
}


function errorHandler(error) {
	console.log(error);
}

// Taken from http://stackoverflow.com/a/105074/515584
// Strictly speaking, it's not a real UUID, but it gets the job done here
// function createUUID() {
// 	function s4() {
// 		return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
// 	}

// 	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
// }