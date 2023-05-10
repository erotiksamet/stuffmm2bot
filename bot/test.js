const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 3131 });

wss.on('connection', function connection(ws) {
  console.log('Client connected');
  
  ws.on('message', function incoming(message) {
    console.log('Received message:', message);
  });
  
  ws.send('Hello, client!');
});
