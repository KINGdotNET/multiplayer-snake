// Initialize the canvas element
const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

// Set up the game variables
const snakeSize = 20;
const gridSize = 20;
const gameWidth = canvas.width;
const gameHeight = canvas.height;
const snakeSpeed = 10;

// Initialize the snake and food arrays
let snakes = [];
let food = [];

// Set up the WebSocket connection
const socket = new WebSocket('ws://localhost:8080');

// Handle incoming messages from the server
socket.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'update') {
    snakes = data.snakes;
    food = data.food;
  } else if (data.type === 'leaderboard') {
    const leaderboard = data.leaderboard;
    // Update the leaderboard display
    document.getElementById('leaderboard').innerHTML = '';
    leaderboard.forEach((entry) => {
      const li = document.createElement('li');
      li.textContent = `${entry.name}: ${entry.score}`;
      document.getElementById('leaderboard').appendChild(li);
    });
  }
};

// Handle keyboard input
document.addEventListener('keydown', (event) => {
  if (event.key === 'ArrowUp') {
    socket.send(JSON.stringify({ type:'move', direction: 'up' }));
  } else if (event.key === 'ArrowDown') {
    socket.send(JSON.stringify({ type:'move', direction: 'down' }));
  } else if (event.key === 'ArrowLeft') {
    socket.send(JSON.stringify({ type:'move', direction: 'left' }));
  } else if (event.key === 'ArrowRight') {
    socket.send(JSON.stringify({ type:'move', direction: 'right' }));
  }
});

// Draw the game state
function draw() {
  ctx.clearRect(0, 0, gameWidth, gameHeight);
  snakes.forEach((snake) => {
    ctx.fillStyle = snake.color;
    ctx.fillRect(snake.x, snake.y, snakeSize, snakeSize);
  });
  food.forEach((food) => {
    ctx.fillStyle ='red';
    ctx.fillRect(food.x, food.y, snakeSize, snakeSize);
  });
  requestAnimationFrame(draw);
}
draw();