import pygame
import random
import socket
import threading

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 20
SPEED = 10

# Set up some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Set up the font
font = pygame.font.Font(None, 36)

# Set up the snake and food
snake = [(200, 200), (220, 200), (240, 200)]
food = (400, 300)

# Set up the leaderboard
leaderboard = []

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('localhost', 12345))
sock.listen(5)

def handle_client(client_socket):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        data = data.decode('utf-8')
        if data.startswith('move'):
            direction = data.split(' ')[1]
            if direction == 'up':
                snake[0] = (snake[0][0], snake[0][1] - BLOCK_SIZE)
            elif direction == 'down':
                snake[0] = (snake[0][0], snake[0][1] + BLOCK_SIZE)
            elif direction == 'left':
                snake[0] = (snake[0][0] - BLOCK_SIZE, snake[0][1])
            elif direction == 'right':
                snake[0] = (snake[0][0] + BLOCK_SIZE, snake[0][1])
        elif data.startswith('score'):
            score = int(data.split(' ')[1])
            leaderboard.append((client_socket.getpeername()[0], score))
            leaderboard.sort(key=lambda x: x[1], reverse=True)
    client_socket.close()

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake[0] = (snake[0][0], snake[0][1] - BLOCK_SIZE)
                elif event.key == pygame.K_DOWN:
                    snake[0] = (snake[0][0], snake[0][1] + BLOCK_SIZE)
                elif event.key == pygame.K_LEFT:
                    snake[0] = (snake[0][0] - BLOCK_SIZE, snake[0][1])
                elif event.key == pygame.K_RIGHT:
                    snake[0] = (snake[0][0] + BLOCK_SIZE, snake[0][1])
        screen.fill(BLACK)
        for pos in snake:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        text = font.render(f'Score: {len(snake)}', True, WHITE)
        screen.blit(text, (10, 10))
        text = font.render('Leaderboard:', True, WHITE)
        screen.blit(text, (10, 50))
        for i, (ip, score) in enumerate(leaderboard):
            text = font.render(f'{i+1}. {ip}: {score}', True, WHITE)
            screen.blit(text, (10, 90 + i * 40))
        pygame.display.flip()
        clock.tick(SPEED)
    pygame.quit()

if __name__ == '__main__':
    main()