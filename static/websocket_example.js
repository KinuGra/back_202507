// WebSocket接続例
const socket = new WebSocket('ws://localhost:8000/ws/room/test123/');

socket.onopen = function(e) {
    console.log('WebSocket接続成功');
    
    // Roomデータ取得
    socket.send(JSON.stringify({
        'type': 'get_room_data'
    }));
    
    // Answerデータ取得
    socket.send(JSON.stringify({
        'type': 'get_answer_data',
        'quiz_id': 1
    }));
};

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    console.log('受信:', data);
    
    if (data.type === 'room_data') {
        console.log('Room data:', data.data);
        updateRoomUI(data.data);
    } else if (data.type === 'answer_data') {
        console.log('Answer data:', data.data);
        updateAnswerUI(data.data);
    }
};

socket.onclose = function(e) {
    console.log('WebSocket接続終了');
};

function updateRoomUI(roomData) {
    // Room UIを更新
    document.getElementById('room-status').textContent = roomData.status;
}

function updateAnswerUI(answerData) {
    // Answer UIを更新
    console.log('Answers:', answerData);
}