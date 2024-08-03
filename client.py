import pygame
import socket

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

# Set up the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 12345))

def main():
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    sock.sendall(b'move up')
                elif event.key == pygame.K_DOWN:
                    sock.sendall(b'move down')
                elif event.key == pygame.K_LEFT:
                    sock.sendall(b'move left')
                elif event.key == pygame.K_RIGHT:
                    sock.sendall(b'move right')
        screen.fill(BLACK)
        for pos in snake:
            pygame.draw.rect(screen, GREEN, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
        text = font.render(f'Score: {len(snake)}', True, WHITE)
        screen.blit(text, (10, 10))
        pygame.display.flip()
        clock.tick(SPEED)
    pygame.quit()

if __name__ == '__main__':
    main()