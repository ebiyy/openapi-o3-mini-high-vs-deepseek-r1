import pygame
import math
import random
from PIL import Image

# 基本設定
WIDTH = 800
HEIGHT = 600
SQUARE_SIZE = 300
BALL_RADIUS = 10
ROTATION_SPEED = 0.5  # 度/秒
RECORD_DURATION = 90  # GIF記録時間（秒）
FPS = 30  # GIFのフレームレート
FRAME_SKIP = 2  # フレームスキップ（メモリ使用量削減用）

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self):
        # ボールの初期位置をランダムに設定
        self.x = random.randint(BALL_RADIUS, SQUARE_SIZE - BALL_RADIUS)
        self.y = random.randint(BALL_RADIUS, SQUARE_SIZE - BALL_RADIUS)
        # ランダムな速度を設定
        self.dx = random.uniform(-5, 5)
        self.dy = random.uniform(-5, 5)
        # ランダムな色を設定
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

    def update(self):
        # 位置の更新
        self.x += self.dx
        self.y += self.dy

        # 衝突判定と反射
        if self.x <= BALL_RADIUS or self.x >= SQUARE_SIZE - BALL_RADIUS:
            self.dx *= -1
        if self.y <= BALL_RADIUS or self.y >= SQUARE_SIZE - BALL_RADIUS:
            self.dy *= -1

def surface_to_pil_image(surface):
    """PyGame surfaceをPIL Imageに変換"""
    image_string = pygame.image.tostring(surface, 'RGB')
    return Image.frombytes('RGB', surface.get_size(), image_string)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("O3 Mini - Rotating Bouncing Balls (90s GIF)")
    clock = pygame.time.Clock()

    balls = []
    last_spawn_time = 0
    angle = 0
    frames = []
    total_frames = RECORD_DURATION * FPS
    frame_count = 0
    save_frame_count = 0

    print(f"記録を開始します（{RECORD_DURATION}秒）...")

    running = True
    while running and frame_count < total_frames:
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 5秒ごとに新しいボールを追加
        if current_time - last_spawn_time > 5000:
            balls.append(Ball())
            last_spawn_time = current_time

        # 正方形の回転
        angle += ROTATION_SPEED
        if angle >= 360:
            angle = 0

        # 画面のクリア
        screen.fill(BLACK)

        # 回転行列の計算
        rad = math.radians(angle)
        cos_val = math.cos(rad)
        sin_val = math.sin(rad)

        # 正方形の中心座標
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # 正方形の頂点を計算
        points = []
        for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            rotated_x = x * SQUARE_SIZE/2 * cos_val - y * SQUARE_SIZE/2 * sin_val
            rotated_y = x * SQUARE_SIZE/2 * sin_val + y * SQUARE_SIZE/2 * cos_val
            points.append((center_x + rotated_x, center_y + rotated_y))

        # 正方形を描画
        pygame.draw.polygon(screen, WHITE, points, 2)

        # ボールの更新と描画
        for ball in balls:
            ball.update()
            # ボールの座標を回転させて描画
            rotated_x = (ball.x - SQUARE_SIZE/2) * cos_val - (ball.y - SQUARE_SIZE/2) * sin_val
            rotated_y = (ball.x - SQUARE_SIZE/2) * sin_val + (ball.y - SQUARE_SIZE/2) * cos_val
            screen_x = center_x + rotated_x
            screen_y = center_y + rotated_y
            pygame.draw.circle(screen, ball.color, (int(screen_x), int(screen_y)), BALL_RADIUS)

        # 残り時間を表示
        font = pygame.font.Font(None, 36)
        remaining_time = RECORD_DURATION - frame_count / FPS
        time_text = f"残り: {remaining_time:.1f}秒"
        text_surface = font.render(time_text, True, WHITE)
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        
        # フレームを間引いてGIF用に保存
        if frame_count % FRAME_SKIP == 0:
            frames.append(surface_to_pil_image(screen))
            save_frame_count += 1
            if save_frame_count % 15 == 0:
                print(f"記録中... {(frame_count / total_frames * 100):.1f}% 完了")

        frame_count += 1
        clock.tick(FPS)

    pygame.quit()

    print("GIFを生成中...")
    if frames:
        frames[0].save(
            'o3_mini_rotating_balls_90s.gif',
            save_all=True,
            append_images=frames[1:],
            optimize=True,
            duration=(1000 * FRAME_SKIP)//FPS,
            loop=0
        )
        print("GIFを保存しました: o3_mini_rotating_balls_90s.gif")

if __name__ == "__main__":
    main()