// Pusher接続例
const pusher = new Pusher('YOUR_PUSHER_KEY', {
  cluster: 'ap3'
});

// Room データの取得とリアルタイム更新
function subscribeToRoom(roomId) {
  const channel = pusher.subscribe(`room-${roomId}`);
  
  // Room データ受信
  channel.bind('room-data', function(data) {
    console.log('Room data received:', data);
    updateRoomUI(data);
  });
  
  // ステータス更新受信
  channel.bind('status-updated', function(data) {
    console.log('Status updated:', data);
    updateStatusUI(data.status);
  });
}

// Answer データの取得とリアルタイム更新
function subscribeToQuiz(quizId) {
  const channel = pusher.subscribe(`quiz-${quizId}`);
  
  channel.bind('answer-data', function(data) {
    console.log('Answer data received:', data);
    updateAnswerUI(data);
  });
}

// API呼び出し例
async function getRoomData(roomId) {
  const response = await fetch(`/api/room-data/?roomId=${roomId}`);
  return response.json();
}

async function getAnswerData(quizId) {
  const response = await fetch(`/api/answer-data/?quizId=${quizId}`);
  return response.json();
}

async function updateRoomStatus(roomId, status) {
  const response = await fetch('/api/update-room-status/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ roomId, status })
  });
  return response.json();
}

// 使用例
subscribeToRoom('room123');
subscribeToQuiz('quiz456');

getRoomData('room123').then(data => console.log(data));
getAnswerData('quiz456').then(data => console.log(data));
updateRoomStatus('room123', 'in_progress');