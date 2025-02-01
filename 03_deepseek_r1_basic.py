import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Square with Bouncing Balls")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Square properties
square_size = 400
square_rect = pygame.Rect((WIDTH - square_size) // 2, (HEIGHT - square_size) // 2, square_size, square_size)
square_angle = 0
square_rotation_speed = 0.5  # Degrees per frame

# Ball properties
ball_radius = 20
balls = []

# Clock
clock = pygame.time.Clock()
last_ball_time = pygame.time.get_ticks()

def rotate_point(cx, cy, x, y, angle):
    """Rotate a point around a center point (cx, cy) by a given angle."""
    angle_rad = math.radians(angle)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    x_new = cx + (x - cx) * cos_a - (y - cy) * sin_a
    y_new = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return x_new, y_new

def get_rotated_square_corners():
    """Get the corners of the rotated square."""
    cx, cy = square_rect.center
    half_size = square_size // 2
    corners = [
        (cx - half_size, cy - half_size),
        (cx + half_size, cy - half_size),
        (cx + half_size, cy + half_size),
        (cx - half_size, cy + half_size)
    ]
    return [rotate_point(cx, cy, x, y, square_angle) for x, y in corners]

def is_point_in_rotated_square(x, y):
    """Check if a point is inside the rotated square."""
    cx, cy = square_rect.center
    x_rot, y_rot = rotate_point(cx, cy, x, y, -square_angle)
    return square_rect.collidepoint(x_rot, y_rot)

def handle_collisions(ball):
    """Handle collisions with the walls of the rotated square."""
    cx, cy = square_rect.center
    x_rot, y_rot = rotate_point(cx, cy, ball['x'], ball['y'], -square_angle)

    if x_rot - ball_radius < square_rect.left:
        ball['dx'] = abs(ball['dx'])
    elif x_rot + ball_radius > square_rect.right:
        ball['dx'] = -abs(ball['dx'])
    if y_rot - ball_radius < square_rect.top:
        ball['dy'] = abs(ball['dy'])
    elif y_rot + ball_radius > square_rect.bottom:
        ball['dy'] = -abs(ball['dy'])

def add_ball():
    """Add a new ball with a random color and velocity."""
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    x = random.randint(square_rect.left + ball_radius, square_rect.right - ball_radius)
    y = random.randint(square_rect.top + ball_radius, square_rect.bottom - ball_radius)
    dx = random.uniform(-3, 3)
    dy = random.uniform(-3, 3)
    balls.append({'x': x, 'y': y, 'dx': dx, 'dy': dy, 'color': color})

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Add a new ball every 5 seconds
    current_time = pygame.time.get_ticks()
    if current_time - last_ball_time > 5000:
        add_ball()
        last_ball_time = current_time

    # Update ball positions
    for ball in balls:
        ball['x'] += ball['dx']
        ball['y'] += ball['dy']
        handle_collisions(ball)

    # Rotate the square
    square_angle = (square_angle + square_rotation_speed) % 360

    # Clear the screen
    screen.fill(WHITE)

    # Draw the rotated square
    corners = get_rotated_square_corners()
    pygame.draw.polygon(screen, BLACK, corners, 2)

    # Draw the balls
    for ball in balls:
        pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball_radius)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()