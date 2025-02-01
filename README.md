# Ball Simulation in a Rotating Square

English | [日本語](README.ja.md)

A project showcasing different implementation approaches and their characteristics using various LLM models.

## File Structure

### Core Implementations
- `01_o3_mini_basic.py` - O3 minimal implementation
- `02_o3_high_oop.py` - O3 object-oriented implementation
- `03_deepseek_r1_basic.py` - DeepSeek R1 basic implementation
- `04_o3_improved_collision.py` - O3 improved version (with ball-to-ball collision)

### GIF Recording Versions (90 seconds)
- `01_o3_mini_basic_90s_gif.py` - O3 minimal implementation with GIF recording
- `02_o3_high_oop_90s_gif.py` - O3 object-oriented implementation with GIF recording
- `03_deepseek_r1_basic_90s_gif.py` - DeepSeek R1 basic implementation with GIF recording
- `04_o3_improved_collision_90s_gif.py` - O3 improved version with GIF recording

## Implementation Features

### O3 Minimal Implementation
- Simple and direct approach
- Basic collision detection
- Minimal code structure

![O3 Minimal Implementation Simulation](o3_mini_rotating_balls_90s.gif)

### O3 Object-Oriented Implementation
- Physics calculations using Vector2D
- Color generation using HSV color space
- Class-based design

![O3 Object-Oriented Implementation Simulation](o3_high_rotating_balls_90s.gif)

### DeepSeek R1 Basic Implementation
- Function-based design
- Basic collision detection
- Practical approach

![DeepSeek R1 Basic Implementation Simulation](deepseek_r1_rotating_balls_90s.gif)

### O3 Improved Version
- Ball-to-ball collision handling
- Physics calculations in local coordinate system
- Perfect elastic collision

![O3 Improved Version Simulation](o3_improved_collision_90s.gif)

## GIF Recording Features
- 90 seconds (1.5 minutes) recording
- 30 FPS
- Memory optimization through frame skipping
- Progress display
- Remaining time display
