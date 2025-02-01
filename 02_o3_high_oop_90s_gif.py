import pygame
import math
import random
import numpy as np
from dataclasses import dataclass
from typing import List, Tuple
from PIL import Image

# 定数定義
@dataclass
class Config:
    WIDTH: int = 800
    HEIGHT: int = 600
    SQUARE_SIZE: int = 300
    BALL_RADIUS: int = 10
    ROTATION_SPEED: float = 0.5  # 度/秒
    FPS: int = 30
    BALL_SPEED_MIN: float = 100.0
    BALL_SPEED_MAX: float = 200.0
    SPAWN_INTERVAL: int = 5000  # ミリ秒
    RECORD_DURATION: int = 90  # GIF記録時間（秒）
    FRAME_SKIP: int = 2  # フレームスキップ（メモリ使用量削減用）

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
        margin = config.BALL_RADIUS * 2
        self.position = Vector2D(
            random.uniform(margin, config.SQUARE_SIZE - margin),
            random.uniform(margin, config.SQUARE_SIZE - margin)
        )
        
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
        self.position = self.position + self.velocity * dt
        
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

def surface_to_pil_image(surface):
    """PyGame surfaceをPIL Imageに変換"""
    image_string = pygame.image.tostring(surface, 'RGB')
    return Image.frombytes('RGB', surface.get_size(), image_string)

class Game:
    """ゲームクラス"""
    def __init__(self):
        pygame.init()
        self.config = Config()
        self.screen = pygame.display.set_mode((self.config.WIDTH, self.config.HEIGHT))
        pygame.display.set_caption("O3 High - Rotating Bouncing Balls (90s GIF)")
        
        self.clock = pygame.time.Clock()
        self.balls: List[Ball] = []
        self.last_spawn_time = 0
        self.angle = 0
        self.frames = []
        self.total_frames = self.config.RECORD_DURATION * self.config.FPS
        self.frame_count = 0
        self.save_frame_count = 0
        
    def handle_events(self) -> bool:
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def update(self, dt: float):
        """ゲーム状態の更新"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_spawn_time > self.config.SPAWN_INTERVAL:
            self.balls.append(Ball(self.config))
            self.last_spawn_time = current_time
        
        for ball in self.balls:
            ball.update(dt, self.config)
        
        self.angle += math.radians(self.config.ROTATION_SPEED)
    
    def render(self):
        """描画処理"""
        self.screen.fill(Colors.BLACK)
        
        # 正方形の描画
        center = Vector2D(self.config.WIDTH / 2, self.config.HEIGHT / 2)
        half_size = self.config.SQUARE_SIZE / 2
        corners = [
            Vector2D(-half_size, -half_size),
            Vector2D(half_size, -half_size),
            Vector2D(half_size, half_size),
            Vector2D(-half_size, half_size)
        ]
        
        rotated_corners = [(center.x + c.rotate(self.angle).x, 
                           center.y + c.rotate(self.angle).y) for c in corners]
        
        pygame.draw.polygon(self.screen, Colors.WHITE, rotated_corners, 2)
        
        # ボールの描画
        for ball in self.balls:
            pos = Vector2D(ball.position.x - half_size, ball.position.y - half_size)
            rotated_pos = pos.rotate(self.angle)
            screen_pos = (int(center.x + rotated_pos.x), 
                         int(center.y + rotated_pos.y))
            pygame.draw.circle(self.screen, ball.color, screen_pos, ball.radius)

        # 残り時間を表示
        font = pygame.font.Font(None, 36)
        remaining_time = self.config.RECORD_DURATION - self.frame_count / self.config.FPS
        time_text = f"残り: {remaining_time:.1f}秒"
        text_surface = font.render(time_text, True, Colors.WHITE)
        self.screen.blit(text_surface, (10, 10))
        
        pygame.display.flip()
    
    def run(self):
        """メインループ"""
        print(f"記録を開始します（{self.config.RECORD_DURATION}秒）...")
        
        running = True
        while running and self.frame_count < self.total_frames:
            dt = self.clock.tick(self.config.FPS) / 1000.0
            
            running = self.handle_events()
            self.update(dt)
            self.render()
            
            # フレームを間引いてGIF用に保存
            if self.frame_count % self.config.FRAME_SKIP == 0:
                self.frames.append(surface_to_pil_image(self.screen))
                self.save_frame_count += 1
                if self.save_frame_count % 15 == 0:
                    print(f"記録中... {(self.frame_count / self.total_frames * 100):.1f}% 完了")
            
            self.frame_count += 1
        
        pygame.quit()
        
        print("GIFを生成中...")
        if self.frames:
            self.frames[0].save(
                'o3_high_rotating_balls_90s.gif',
                save_all=True,
                append_images=self.frames[1:],
                optimize=True,
                duration=(1000 * self.config.FRAME_SKIP)//self.config.FPS,
                loop=0
            )
            print("GIFを保存しました: o3_high_rotating_balls_90s.gif")

if __name__ == "__main__":
    game = Game()
    game.run()