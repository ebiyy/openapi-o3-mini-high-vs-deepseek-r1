import pygame
import math
import random

# 基本設定
WIDTH = 800
HEIGHT = 600
SQUARE_SIZE = 300
BALL_RADIUS = 10
ROTATION_SPEED = 0.5  # 度/秒

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

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("O3 Mini - Rotating Bouncing Balls")
    clock = pygame.time.Clock()

    balls = []
    last_spawn_time = 0
    angle = 0

    running = True
    while running:
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

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()