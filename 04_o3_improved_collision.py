import pygame
import math
import random

# ---------------------------
# グローバル定数・設定
# ---------------------------
WIDTH, HEIGHT = 800, 600
SQUARE_SIZE = 400         # コンテナ（正方形）の一辺の長さ
SQUARE_HALF = SQUARE_SIZE / 2
BALL_RADIUS = 10          # ボールの半径（ローカル座標系）
BALL_SPEED = 200          # ボールの初速（ピクセル/秒、ローカル座標系）
ROTATION_SPEED = math.radians(10)  # 正方形は1秒間に10°回転

# 正方形は画面中央に描画する
SQUARE_CENTER = (WIDTH // 2, HEIGHT // 2)

# ---------------------------
# ボールクラス（ローカル座標系）
# ---------------------------
class Ball:
    def __init__(self, x, y, vx, vy, color):
        """
        x, y: 正方形内での初期位置（原点は正方形の中心）
        vx, vy: 速度（ローカル座標系での単位：ピクセル/秒）
        color: (R, G, B) のタプル
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color

    def update(self, dt):
        # ローカル座標系において位置を更新
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 正方形の壁との衝突判定（ローカル座標系の境界は ±(SQUARE_HALF - BALL_RADIUS)）
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
# 球同士の衝突処理（等質な完全弾性衝突の近似）
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
                # dist==0 となる場合（極めて稀）には、任意の単位ベクトルを使う
                if dist == 0:
                    nx, ny = 1, 0
                else:
                    nx = dx / dist
                    ny = dy / dist

                # 重なり量の補正：各ボールを半分ずつ押し戻す
                overlap = 2 * BALL_RADIUS - dist
                correction = overlap / 2
                b1.x += nx * correction
                b1.y += ny * correction
                b2.x -= nx * correction
                b2.y -= ny * correction

                # 衝突応答（速度の交換：ボール同士が近づいている場合のみ）
                # 相対速度の正規方向成分を計算
                v_rel = (b1.vx - b2.vx) * nx + (b1.vy - b2.vy) * ny
                if v_rel < 0:  # すでに離れている場合は何もしない
                    impulse = -v_rel  # 衝突による速度補正量（等質の場合）
                    b1.vx += impulse * nx
                    b1.vy += impulse * ny
                    b2.vx -= impulse * nx
                    b2.vy -= impulse * ny

# ---------------------------
# メインループ
# ---------------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("O3 Improved - 回転する正方形内の弾むボール（球同士の衝突付き）")
    clock = pygame.time.Clock()

    balls = []            # ローカル座標系でのボールリスト
    ball_spawn_timer = 0  # 5秒ごとに新しいボールを生成するためのタイマー
    angle = 0             # 正方形の現在の回転角（ラジアン）

    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # フレーム間の経過時間（秒単位）

        # --- イベント処理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- 正方形（コンテナ）の回転更新 ---
        angle += ROTATION_SPEED * dt

        # --- 各ボールの位置更新（壁との衝突も内部で処理） ---
        for ball in balls:
            ball.update(dt)

        # --- 球同士の衝突処理 ---
        resolve_ball_collisions(balls)

        # --- 5秒ごとに新たなボールを生成 ---
        ball_spawn_timer += dt
        if ball_spawn_timer >= 5:
            ball_spawn_timer = 0

            # 壁から十分離れたランダムなローカル座標上の位置
            x = random.uniform(-SQUARE_HALF + BALL_RADIUS, SQUARE_HALF - BALL_RADIUS)
            y = random.uniform(-SQUARE_HALF + BALL_RADIUS, SQUARE_HALF - BALL_RADIUS)

            # ランダムな方向へ初速度を与える
            theta = random.uniform(0, 2 * math.pi)
            vx = BALL_SPEED * math.cos(theta)
            vy = BALL_SPEED * math.sin(theta)

            # 鮮やかなランダムな色を生成
            color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
            balls.append(Ball(x, y, vx, vy, color))

        # --- 描画 ---
        screen.fill((30, 30, 30))  # 暗い背景で画面をクリア

        # 回転後の正方形の各頂点（ローカル座標系での頂点は固定）
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
            # ローカル座標から回転を加えてスクリーン座標へ変換
            wx = SQUARE_CENTER[0] + lx * cos_a - ly * sin_a
            wy = SQUARE_CENTER[1] + lx * sin_a + ly * cos_a
            world_corners.append((wx, wy))

        # 正方形コンテナを描画（アウトラインのみ）
        pygame.draw.polygon(screen, (200, 200, 200), world_corners, 3)

        # 各ボールの描画（ローカル座標→スクリーン座標へ変換）
        for ball in balls:
            wx = SQUARE_CENTER[0] + ball.x * cos_a - ball.y * sin_a
            wy = SQUARE_CENTER[1] + ball.x * sin_a + ball.y * cos_a
            pygame.draw.circle(screen, ball.color, (int(wx), int(wy)), BALL_RADIUS)

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()