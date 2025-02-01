import pygame
import random
import math
from PIL import Image

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DeepSeek R1 - Rotating Square with Bouncing Balls (90s GIF)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Square properties
square_size = 400
square_rect = pygame.Rect((WIDTH - square_size) // 2, (HEIGHT - square_size) // 2, square_size, square_size)
square_rotation_speed = 0.5  # Degrees per frame

# Ball properties
ball_radius = 20
balls = []

# Recording properties
RECORD_DURATION = 90  # seconds
FPS = 30
FRAME_SKIP = 2  # Frame skip for memory optimization

def rotate_point(cx, cy, x, y, angle):
    """Rotate a point around a center point (cx, cy) by a given angle."""
    angle_rad = math.radians(angle)
    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)
    x_new = cx + (x - cx) * cos_a - (y - cy) * sin_a
    y_new = cy + (x - cx) * sin_a + (y - cy) * cos_a
    return x_new, y_new

def get_rotated_square_corners(angle):
    """Get the corners of the rotated square."""
    cx, cy = square_rect.center
    half_size = square_size // 2
    corners = [
        (cx - half_size, cy - half_size),
        (cx + half_size, cy - half_size),
        (cx + half_size, cy + half_size),
        (cx - half_size, cy + half_size)
    ]
    return [rotate_point(cx, cy, x, y, angle) for x, y in corners]

def is_point_in_rotated_square(x, y, angle):
    """Check if a point is inside the rotated square."""
    cx, cy = square_rect.center
    x_rot, y_rot = rotate_point(cx, cy, x, y, -angle)
    return square_rect.collidepoint(x_rot, y_rot)

def handle_collisions(ball, angle):
    """Handle collisions with the walls of the rotated square."""
    cx, cy = square_rect.center
    x_rot, y_rot = rotate_point(cx, cy, ball['x'], ball['y'], -angle)

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

def surface_to_pil_image(surface):
    """Convert Pygame surface to PIL Image"""
    image_string = pygame.image.tostring(surface, 'RGB')
    return Image.frombytes('RGB', surface.get_size(), image_string)

# Main loop
def main():
    clock = pygame.time.Clock()
    last_ball_time = 0
    angle = 0  # Initialize angle here
    frames = []
    total_frames = RECORD_DURATION * FPS
    frame_count = 0
    save_frame_count = 0

    print(f"記録を開始します（{RECORD_DURATION}秒）...")

    running = True
    while running and frame_count < total_frames:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
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
            handle_collisions(ball, angle)

        # Rotate the square
        angle = (angle + square_rotation_speed) % 360

        # Clear the screen
        screen.fill(WHITE)

        # Draw the rotated square
        corners = get_rotated_square_corners(angle)
        pygame.draw.polygon(screen, BLACK, corners, 2)

        # Draw the balls
        for ball in balls:
            pygame.draw.circle(screen, ball['color'], (int(ball['x']), int(ball['y'])), ball_radius)

        # Draw remaining time
        font = pygame.font.Font(None, 36)
        remaining_time = RECORD_DURATION - frame_count / FPS
        time_text = f"残り: {remaining_time:.1f}秒"
        text_surface = font.render(time_text, True, BLACK)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()

        # Save frame for GIF
        if frame_count % FRAME_SKIP == 0:
            frames.append(surface_to_pil_image(screen))
            save_frame_count += 1
            if save_frame_count % 15 == 0:
                print(f"記録中... {(frame_count / total_frames * 100):.1f}% 完了")

        frame_count += 1

    pygame.quit()

    print("GIFを生成中...")
    if frames:
        frames[0].save(
            'deepseek_r1_rotating_balls_90s.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=(1000 * FRAME_SKIP)//FPS,
            loop=0
        )
        print("GIFを保存しました: deepseek_r1_rotating_balls_90s.gif")

if __name__ == '__main__':
    main()