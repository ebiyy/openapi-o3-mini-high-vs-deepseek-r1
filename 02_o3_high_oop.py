import pygame
import math
import random
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple

# 定数定義
@dataclass
class Config:
    WIDTH: int = 800
    HEIGHT: int = 600
    SQUARE_SIZE: int = 300
    BALL_RADIUS: int = 10
    ROTATION_SPEED: float = 0.5  # 度/秒
    FPS: int = 60
    BALL_SPEED_MIN: float = 100.0
    BALL_SPEED_MAX: float = 200.0
    SPAWN_INTERVAL: int = 5000  # ミリ秒

# 色の定義
class Colors:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    
    @staticmethod
    def random_bright_color() -> Tuple[int, int, int]:
        """明るいランダムな色を生成"""
        hue = random.random()
        saturation = random.uniform(0.5, 1.0)
        value = random.uniform(0.8, 1.0)
        
        # HSV から RGB への変換
        h = hue * 6
        f = h - int(h)
        p = value * (1 - saturation)
        q = value * (1 - f * saturation)
        t = value * (1 - (1 - f) * saturation)
        
        if int(h) == 0:
            r, g, b = value, t, p
        elif int(h) == 1:
            r, g, b = q, value, p
        elif int(h) == 2:
            r, g, b = p, value, t
        elif int(h) == 3:
            r, g, b = p, q, value
        elif int(h) == 4:
            r, g, b = t, p, value
        else:
            r, g, b = value, p, q
            
        return (int(r * 255), int(g * 255), int(b * 255))

class Vector2D:
    """2次元ベクトルクラス"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def dot(self, other: 'Vector2D') -> float:
        return self.x * other.x + self.y * other.y
    
    def length(self) -> float:
        return math.sqrt(self.dot(self))
    
    def normalize(self) -> 'Vector2D':
        length = self.length()
        if length > 0:
            return self * (1.0 / length)
        return Vector2D(0, 0)
    
    def rotate(self, angle: float) -> 'Vector2D':
        """ベクトルを指定角度（ラジアン）回転"""
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        return Vector2D(
            self.x * cos_val - self.y * sin_val,
            self.x * sin_val + self.y * cos_val
        )

class Ball:
    """ボールクラス"""
    def __init__(self, config: Config):
        # 正方形内のランダムな位置に配置
        margin = config.BALL_RADIUS * 2
        self.position = Vector2D(
            random.uniform(margin, config.SQUARE_SIZE - margin),
            random.uniform(margin, config.SQUARE_SIZE - margin)
        )
        
        # ランダムな方向と速度を設定
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(config.BALL_SPEED_MIN, config.BALL_SPEED_MAX)
        self.velocity = Vector2D(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        
        self.radius = config.BALL_RADIUS
        self.color = Colors.random_bright_color()
        
    def update(self, dt: float, config: Config):
        """ボールの位置を更新"""
        # 位置の更新
        self.position = self.position + self.velocity * dt
        
        # 衝突判定と反射
        margin = self.radius
        if self.position.x < margin:
            self.position.x = margin
            self.velocity.x = abs(self.velocity.x)
        elif self.position.x > config.SQUARE_SIZE - margin:
            self.position.x = config.SQUARE_SIZE - margin
            self.velocity.x = -abs(self.velocity.x)
            
        if self.position.y < margin:
            self.position.y = margin
            self.velocity.y = abs(self.velocity.y)
        elif self.position.y > config.SQUARE_SIZE - margin:
            self.position.y = config.SQUARE_SIZE - margin
            self.velocity.y = -abs(self.velocity.y)

class RotatingSquare:
    """回転する正方形クラス"""
    def __init__(self, config: Config):
        self.size = config.SQUARE_SIZE
        self.angle = 0.0  # ラジアン
        self.center = Vector2D(config.WIDTH / 2, config.HEIGHT / 2)
        
    def update(self, dt: float, rotation_speed: float):
        """正方形の回転を更新"""
        self.angle += math.radians(rotation_speed) * dt
        if self.angle >= 2 * math.pi:
            self.angle -= 2 * math.pi
            
    def get_corners(self) -> List[Tuple[float, float]]:
        """回転後の正方形の頂点座標を取得"""
        half_size = self.size / 2
        corners = []
        for x, y in [(-1, -1), (1, -1), (1, 1), (-1, 1)]:
            point = Vector2D(x * half_size, y * half_size).rotate(self.angle)
            corners.append((
                self.center.x + point.x,
                self.center.y + point.y
            ))
        return corners
    
    def world_to_screen(self, position: Vector2D) -> Tuple[float, float]:
        """ローカル座標をスクリーン座標に変換"""
        rotated = Vector2D(
            position.x - self.size/2,
            position.y - self.size/2
        ).rotate(self.angle)
        return (
            self.center.x + rotated.x,
            self.center.y + rotated.y
        )

class Game:
    """ゲームクラス"""
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("O3 High - Rotating Bouncing Balls")
        
        self.clock = pygame.time.Clock()
        self.balls: List[Ball] = []
        self.square = RotatingSquare(self.config)
        self.last_spawn_time = 0
        
    def handle_events(self) -> bool:
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def update(self, dt: float):
        """ゲーム状態の更新"""
        current_time = pygame.time.get_ticks()
        
        # 新しいボールの生成
        if current_time - self.last_spawn_time > self.config.SPAWN_INTERVAL:
            self.balls.append(Ball(self.config))
            self.last_spawn_time = current_time
        
        # ボールの更新
        for ball in self.balls:
            ball.update(dt, self.config)
        
        # 正方形の回転
        self.square.update(dt, self.config.ROTATION_SPEED)
    
    def render(self):
        """描画処理"""
        self.screen.fill(Colors.BLACK)
        
        # 正方形の描画
        pygame.draw.polygon(
            self.screen,
            Colors.WHITE,
            self.square.get_corners(),
            2
        )
        
        # ボールの描画
        for ball in self.balls:
            screen_pos = self.square.world_to_screen(ball.position)
            pygame.draw.circle(
                self.screen,
                ball.color,
                (int(screen_pos[0]), int(screen_pos[1])),
                ball.radius
            )
        
        pygame.display.flip()
    
    def run(self):
        """メインループ"""
        running = True
        while running:
            dt = self.clock.tick(self.config.FPS) / 1000.0
            
            running = self.handle_events()
            self.update(dt)
            self.render()
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()