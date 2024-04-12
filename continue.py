import pygame
import sys
import random
import time  # 添加时间模块

pygame.init()

GRID_SIZE = 50
GRID_ROWS = 20
GRID_COLS = 20
WINDOW_SIZE = (GRID_SIZE * GRID_COLS, GRID_SIZE * GRID_ROWS)

screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Keyboard-Controlled Grid Movement")

CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# 初始化小球位置到窗口中心
ball_pos = [WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2]
ball_speed = 2  # 设置速度为一个格子的大小

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    target_list = ['1', '2', '3', '4']
    label = random.randint(1, 4)

    # 保存原始的ball_pos
    original_ball_pos = ball_pos.copy()

    if label == 1:
        target_pos = [ball_pos[0] + 2*GRID_SIZE, ball_pos[1]]
        # 边界检查
        if target_pos[0] > WINDOW_SIZE[0]:
            target_pos[0] = WINDOW_SIZE[0]
    elif label == 2:
        target_pos = [ball_pos[0] - 2*GRID_SIZE, ball_pos[1]]
        # 边界检查
        if target_pos[0] < 0:
            target_pos[0] = 0
    elif label == 3:
        target_pos = [ball_pos[0], ball_pos[1] - 2*GRID_SIZE]
        # 边界检查
        if target_pos[1] < 0:
            target_pos[1] = 0
    elif label == 4:
        target_pos = [ball_pos[0], ball_pos[1] + 2*GRID_SIZE]
        # 边界检查
        if target_pos[1] > WINDOW_SIZE[1]:
            target_pos[1] = WINDOW_SIZE[1]

    # 使用更小的步进值
    steps = 30

    for step in range(steps):
        # 计算每个步骤中的小球位置，使用整数运算
        ball_pos[0] = original_ball_pos[0] + (target_pos[0] - original_ball_pos[0]) * (step + 1) // steps
        ball_pos[1] = original_ball_pos[1] + (target_pos[1] - original_ball_pos[1]) * (step + 1) // steps

        # 绘制背景网格线
        screen.fill(WHITE)
        for row in range(GRID_ROWS + 1):
            pygame.draw.line(screen, CYAN, (0, row * GRID_SIZE), (WINDOW_SIZE[0], row * GRID_SIZE), 1)
        for col in range(GRID_COLS + 1):
            pygame.draw.line(screen, CYAN, (col * GRID_SIZE, 0), (col * GRID_SIZE, WINDOW_SIZE[1]), 1)

        # 绘制小球，转换为浮点数
        pygame.draw.circle(screen, GREEN, (float(ball_pos[0]), float(ball_pos[1])), GRID_SIZE // 4)

        # 显示最终结果
        pygame.display.flip()

        # 加入短暂延迟
        time.sleep(0.05)

    pygame.time.Clock().tick(30)
