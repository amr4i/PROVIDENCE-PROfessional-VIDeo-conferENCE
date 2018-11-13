var localVideo;
var localStream;
var remoteVideo;
var peerConnection;
var uuid;
var username;
var serverConnection;

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


function gotMessageFromServer(message) {
	if(!peerConnection) start(false);

	console.log(message);
	console.log('************');
	// console.log(message.data);
	// var signal = JSON.parse(message);
	var signal = message;
	console.log(signal);

	// Ignore messages from ourself
	if(signal.uuid == username) return;
	// if(signal.uuid == uuid) return;

	if(signal.sdp) {
		peerConnection.setRemoteDescription(new RTCSessionDescription(signal.sdp)).then(function() {
		// Only create answers in response to offers
		if(signal.sdp.type == 'offer') {
			peerConnection.createAnswer().then(createdDescription).catch(errorHandler);
		}
    }).catch(errorHandler);
	} else if(signal.ice) {
		peerConnection.addIceCandidate(new RTCIceCandidate(signal.ice)).catch(errorHandler);
	}
}

function gotIceCandidate(event) {
	if(event.candidate != null) {
		// serverConnection.send(JSON.stringify({'ice': event.candidate, 'uuid': uuid}));
		// serverConnection.emit('ice candidate', {'ice': event.candidate, 'uuid': uuid});
		serverConnection.emit('ice candidate', {'ice': event.candidate, 'uuid': uuid});
	}
}

function createdDescription(description) {
	console.log('got description');
	console.log('Hi');
	peerConnection.setLocalDescription(description).then(function() {
		// serverConnection.send(JSON.stringify({'sdp': peerConnection.localDescription, 'uuid': uuid}));
		serverConnection.emit('client description', {'sdp': peerConnection.localDescription, 'uuid': uuid});
	}).catch(errorHandler);
}

function gotRemoteStream(event) {
	console.log('got remote stream');
	remoteVideo.srcObject = event.streams[0];
}
function start(isCaller) {
	peerConnection = new RTCPeerConnection(peerConnectionConfig);
	peerConnection.onicecandidate = gotIceCandidate;
	peerConnection.ontrack = gotRemoteStream;
	peerConnection.addStream(localStream);

	if(isCaller) {
		peerConnection.createOffer().then(createdDescription).catch(errorHandler);
	}
}



function errorHandler(error) {
	console.log(error);
}

// Taken from http://stackoverflow.com/a/105074/515584
// Strictly speaking, it's not a real UUID, but it gets the job done here
function createUUID() {
	function s4() {
		return Math.floor((1 + Math.random()) * 0x10000).toString(16).substring(1);
	}

	return s4() + s4() + '-' + s4() + '-' + s4() + '-' + s4() + '-' + s4() + s4() + s4();
}