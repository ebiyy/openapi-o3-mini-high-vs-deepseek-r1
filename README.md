# 回転する正方形内のボールシミュレーション

各モデルの実装とその特徴を示すプロジェクトです。

## ファイル構成

### 基本実装
- `01_o3_mini_basic.py` - O3の最小限の実装
- `02_o3_high_oop.py` - O3のオブジェクト指向実装
- `03_deepseek_r1_basic.py` - DeepSeek R1の基本実装
- `04_o3_improved_collision.py` - O3の改良版（ボール同士の衝突対応）

### GIF記録バージョン（90秒）
- `01_o3_mini_basic_90s_gif.py` - O3ミニマル実装のGIF記録版
- `02_o3_high_oop_90s_gif.py` - O3オブジェクト指向実装のGIF記録版
- `03_deepseek_r1_basic_90s_gif.py` - DeepSeek R1基本実装のGIF記録版
- `04_o3_improved_collision_90s_gif.py` - O3改良版のGIF記録版

## 各実装の特徴

### O3 ミニマル実装
- シンプルで直接的なアプローチ
- 基本的な衝突判定
- 最小限のコード構造

![O3 ミニマル実装のシミュレーション](o3_mini_rotating_balls_90s.gif)

### O3 オブジェクト指向実装
- Vector2Dによる物理計算
- HSV色空間による色生成
- クラスベースの設計

![O3 オブジェクト指向実装のシミュレーション](o3_high_rotating_balls_90s.gif)

### DeepSeek R1基本実装
- 関数ベースの設計
- 基本的な衝突判定
- 実用的なアプローチ

![DeepSeek R1基本実装のシミュレーション](deepseek_r1_rotating_balls_90s.gif)

### O3 改良版
- ボール同士の衝突対応
- ローカル座標系での物理計算
- 完全弾性衝突

![O3 改良版のシミュレーション](o3_improved_collision_90s.gif)

## GIF記録機能
- 90秒（1分30秒）の記録
- 30FPS
- フレームスキップによるメモリ最適化
- 進捗表示
