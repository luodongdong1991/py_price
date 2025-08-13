import pygame
import random
import time

# 初始化 Pygame
pygame.init()

# 设置窗口大小
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("贪吃蛇游戏")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 蛇的大小和速度
snake_block = 20
snake_speed = 15

# 蛇的初始位置和长度
snake_list = []
snake_length = 1
snake_x = width // 2
snake_y = height // 2

# 食物的初始位置
food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block

# 方向控制
x_change = 0
y_change = 0

# 分数
score = 0

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change = -snake_block
                y_change = 0
            elif event.key == pygame.K_RIGHT:
                x_change = snake_block
                y_change = 0
            elif event.key == pygame.K_UP:
                x_change = 0
                y_change = -snake_block
            elif event.key == pygame.K_DOWN:
                x_change = 0
                y_change = snake_block

    # 更新蛇的位置
    snake_x += x_change
    snake_y += y_change

    # 检查是否撞墙
    if snake_x >= width or snake_x < 0 or snake_y >= height or snake_y < 0:
        running = False

    # 检查是否吃到食物
    if snake_x == food_x and snake_y == food_y:
        food_x = round(random.randrange(0, width - snake_block) / snake_block) * snake_block
        food_y = round(random.randrange(0, height - snake_block) / snake_block) * snake_block
        snake_length += 1
        score += 1

    # 更新蛇的身体
    snake_head = [snake_x, snake_y]
    snake_list.append(snake_head)
    if len(snake_list) > snake_length:
        del snake_list[0]

    # 检查是否撞到自己
    for segment in snake_list[:-1]:
        if segment == snake_head:
            running = False

    # 绘制背景
    window.fill(BLACK)

    # 绘制蛇
    for segment in snake_list:
        pygame.draw.rect(window, GREEN, [segment[0], segment[1], snake_block, snake_block])

    # 绘制食物
    pygame.draw.rect(window, RED, [food_x, food_y, snake_block, snake_block])

    # 显示分数
    font = pygame.font.SysFont(None, 35)
    score_text = font.render("得分: " + str(score), True, WHITE)
    window.blit(score_text, [0, 0])

    # 更新屏幕
    pygame.display.update()

    # 控制游戏速度
    pygame.time.Clock().tick(snake_speed)

# 游戏结束
pygame.quit()