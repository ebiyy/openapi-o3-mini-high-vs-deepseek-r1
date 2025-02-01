import pygame
import math
import random
from PIL import Image
import io

# ---------------------------
# グローバル定数・設定
# ---------------------------
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 400
SQUARE_HALF = SQUARE_SIZE / 2
BALL_RADIUS = 10
BALL_SPEED = 200
ROTATION_SPEED = math.radians(10)
SQUARE_CENTER = (WIDTH // 2, HEIGHT // 2)
RECORD_DURATION = 90  # GIF記録時間（秒）
FPS = 30  # GIFのフレームレート

# メモリ使用量を抑えるため、フレームを間引く
FRAME_SKIP = 2  # 2フレームに1フレームを保存

# ---------------------------
# ボールクラス（ローカル座標系）
# ---------------------------
class Ball:
    def __init__(self, x, y, vx, vy, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

        if self.x > SQUARE_HALF - BALL_RADIUS:
            self.x = SQUARE_HALF - BALL_RADIUS
            self.vx = -self.vx
        elif self.x < -SQUARE_HALF + BALL_RADIUS:
            self.x = -SQUARE_HALF + BALL_RADIUS
            self.vx = -self.vx

        if self.y > SQUARE_HALF - BALL_RADIUS:
            self.y = SQUARE_HALF - BALL_RADIUS
            self.vy = -self.vy
        elif self.y < -SQUARE_HALF + BALL_RADIUS:
            self.y = -SQUARE_HALF + BALL_RADIUS
            self.vy = -self.vy

# ---------------------------
# 球同士の衝突処理
# ---------------------------
def resolve_ball_collisions(balls):
    n = len(balls)
    for i in range(n):
        for j in range(i + 1, n):
            b1 = balls[i]
            b2 = balls[j]
            dx = b1.x - b2.x
            dy = b1.y - b2.y
            dist = math.hypot(dx, dy)
            if dist < 2 * BALL_RADIUS:
                if dist == 0:
                    nx, ny = 1, 0
                else:
                    nx = dx / dist
                    ny = dy / dist

                overlap = 2 * BALL_RADIUS - dist
                correction = overlap / 2
                b1.x += nx * correction
                b1.y += ny * correction
                b2.x -= nx * correction
                b2.y -= ny * correction

                v_rel = (b1.vx - b2.vx) * nx + (b1.vy - b2.vy) * ny
                if v_rel < 0:
                    impulse = -v_rel
                    b1.vx += impulse * nx
                    b1.vy += impulse * ny
                    b2.vx -= impulse * nx
                    b2.vy -= impulse * ny

def surface_to_pil_image(surface):
    """PyGame surfaceをPIL Imageに変換"""
    image_string = pygame.image.tostring(surface, 'RGB')
    return Image.frombytes('RGB', surface.get_size(), image_string)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("O3 Improved - 回転する正方形内の弾むボール（90秒GIF記録）")
    clock = pygame.time.Clock()

    balls = []
    ball_spawn_timer = 0
    angle = 0
    frames = []  # GIFフレームを保存するリスト
    total_frames = RECORD_DURATION * FPS
    frame_count = 0
    save_frame_count = 0

    print(f"記録を開始します（{RECORD_DURATION}秒）...")

    running = True
    while running and frame_count < total_frames:
        dt = 1.0 / FPS  # 固定デルタタイム

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        angle += ROTATION_SPEED * dt

        for ball in balls:
            ball.update(dt)

        resolve_ball_collisions(balls)

        ball_spawn_timer += dt
        if ball_spawn_timer >= 5:
            ball_spawn_timer = 0
            x = random.uniform(-SQUARE_HALF + BALL_RADIUS, SQUARE_HALF - BALL_RADIUS)
            y = random.uniform(-SQUARE_HALF + BALL_RADIUS, SQUARE_HALF - BALL_RADIUS)
            theta = random.uniform(0, 2 * math.pi)
            vx = BALL_SPEED * math.cos(theta)
            vy = BALL_SPEED * math.sin(theta)
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            balls.append(Ball(x, y, vx, vy, color))

        screen.fill((30, 30, 30))

        local_corners = [
            (-SQUARE_HALF, -SQUARE_HALF),
            ( SQUARE_HALF, -SQUARE_HALF),
            ( SQUARE_HALF,  SQUARE_HALF),
            (-SQUARE_HALF,  SQUARE_HALF)
        ]
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        world_corners = []
        for lx, ly in local_corners:
            wx = SQUARE_CENTER[0] + lx * cos_a - ly * sin_a
            wy = SQUARE_CENTER[1] + lx * sin_a + ly * cos_a
            world_corners.append((wx, wy))

        pygame.draw.polygon(screen, (200, 200, 200), world_corners, 3)

        for ball in balls:
            wx = SQUARE_CENTER[0] + ball.x * cos_a - ball.y * sin_a
            wy = SQUARE_CENTER[1] + ball.x * sin_a + ball.y * cos_a
            pygame.draw.circle(screen, ball.color, (int(wx), int(wy)), BALL_RADIUS)

        # 残り時間を表示
        font = pygame.font.Font(None, 36)
        remaining_time = RECORD_DURATION - frame_count / FPS
        time_text = f"残り: {remaining_time:.1f}秒"
        text_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        
        # フレームを間引いてGIF用に保存
        if frame_count % FRAME_SKIP == 0:
            frames.append(surface_to_pil_image(screen))
            save_frame_count += 1
            if save_frame_count % 15 == 0:  # 15フレームごとに進捗を表示
                print(f"記録中... {(frame_count / total_frames * 100):.1f}% 完了")

        frame_count += 1
        clock.tick(FPS)

    pygame.quit()

    print("GIFを生成中...")
    if frames:
        frames[0].save(
            'rotating_balls_90s.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=(1000 * FRAME_SKIP)//FPS,  # フレームスキップを考慮した時間
            loop=0
        )
        print("GIFを保存しました: rotating_balls_90s.gif")

if __name__ == '__main__':
    main()