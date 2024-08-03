const WebSocket = require('ws');
const wss = new WebSocket.Server({ port: 8080 });

// Initialize the game state
const snakes = [];
const food = [];
const leaderboard = [];

// Handle incoming connections
wss.on('connection', (ws) => {
  console.log('New connection');

  // Handle incoming messages
  ws.on('message', (message) => {
    const data = JSON.parse(message);
    if (data.type ==='move') {
      const snake = snakes.find((snake) => snake.id === data.id);
      if (snake) {
        snake.x += data.direction === 'right'? snakeSize : -snakeSize;
        snake.y += data.direction === 'down'? snakeSize : -snakeSize;
      }
    }
  });

  // Handle disconnections
  ws.on('close', () => {
    console.log('Connection closed');
  });
});

// Update the game state
setInterval(() => {
  // Move the snakes
  snakes.forEach((snake) => {
    snake.x += snakeSpeed;
    if (snake.x > gameWidth) {
      snake.x = 0;
    } else if (snake.x < 0) {
      snake.x = gameWidth;
    }
  });

  // Check for collisions
  snakes.forEach((snake) => {
    if (snake.x < 0 || snake.x > gameWidth || snake.y < 0 || snake.y > gameHeight) {
      // Remove the snake from the game
      snakes.splice(snakes.indexOf(snake), 1);
    }
  });

  // Update the leaderboard
  leaderboard.sort((a, b) => b.score - a.score);

  // Send the updated game state to all clients
  wss.clients.forEach((client) => {
    client.send(JSON.stringify({ type: 'update', snakes, food, leaderboard }));
  });
}, 1000 / 60);
