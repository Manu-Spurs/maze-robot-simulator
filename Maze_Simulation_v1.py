import pygame
import random
import sys
import math

# 初始化pygame
pygame.init()

# 常量定义
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
MAZE_SIZE = 8
CELL_SIZE = WINDOW_WIDTH // MAZE_SIZE

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
DARK_GREEN = (0, 150, 0)
LIGHT_BLUE = (100, 150, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

class Maze:
    def __init__(self):
        self.grid = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
        # 按照精确位置设置所有特殊标记点
        self.castle = (7, 4)  # 城堡位置（起点）
        self.goal = (0, 3)    # 棋盘格终点
        self.robot_pos = (7, 4)  # 机器人位置（在绿色方块起点上）
        
        # 数字方块位置
        self.numbered_squares = {
            1: (7, 6),  # 数字1
            2: (6, 1),  # 数字2
            3: (2, 1),  # 数字3
            4: (0, 7)   # 数字4
        }
        
        # 字母圆圈位置
        self.lettered_circles = {
            'A': (7, 3),  # 字母A
            'B': (4, 0),  # 字母B
            'C': (0, 0),  # 字母C
            'D': (3, 5)   # 字母D
        }
        
        # 计时器
        self.timer = 0
        
        # 保存原始迷宫状态
        self.original_walls = None
        
        # 是否显示特殊标记（字母和数字）
        self.show_special_markers = True
        
        # 生成严格按照新图片的迷宫
        self.generate_exact_maze()
        
        # 保存当前迷宫为原始迷宫
        self.save_as_original()
    
    def generate_exact_maze(self):
        """严格按照图片生成迷宫，所有位置都是通路，墙壁用红色线条表示"""
        # 所有位置都是通路
        for i in range(MAZE_SIZE):
            for j in range(MAZE_SIZE):
                self.grid[i][j] = 0
        
        # 创建严格按照图片的墙壁布局
        self.create_exact_walls()
    
    def create_exact_walls(self):
        """创建严格按照图片的墙壁布局"""
        self.walls = {
            'horizontal': [],  # 水平墙壁
            'vertical': []    # 垂直墙壁
        }
        
        # 添加边界墙壁
        self.add_boundary_walls()
        
        # 严格按照图片添加内部墙壁
        self.add_exact_internal_walls()
    
    def add_boundary_walls(self):
        """添加边界墙壁"""
        # 外边界墙壁
        for i in range(MAZE_SIZE):
            # 左边界
            self.walls['vertical'].append((i, 0))
            # 右边界
            self.walls['vertical'].append((i, MAZE_SIZE))
        
        for j in range(MAZE_SIZE):
            # 上边界
            self.walls['horizontal'].append((0, j))
            # 下边界
            self.walls['horizontal'].append((MAZE_SIZE, j))
    
    def add_exact_internal_walls(self):
        """严格按照用户描述添加精确的墙壁位置"""
        # 水平墙壁 (行, 列)
        horizontal_walls = [
            # 0,1之间的水平墙在第0,1,3,4,5列
            (1, 0), (1, 1), (1, 3), (1, 4), (1, 5),
            # 1,2之间的水平墙在第2,4,5,6列
            (2, 2), (2, 4), (2, 5), (2, 6),
            # 2,3之间的水平墙在第1,3,5列
            (3, 1), (3, 3), (3, 5),
            # 3,4之间的水平墙在第0,2列
            (4, 0), (4, 2),
            # 4,5之间的水平墙在第1,3列
            (5, 1), (5, 3),
            # 5,6之间的水平墙在第4,5,6,7列
            (6, 4), (6, 5), (6, 6), (6, 7),
            # 7,8之间的水平墙在第1,6列
            (8, 1), (8, 6),
            # 6,7行之间的水平墙，1,6列添加水平墙
            (7, 1), (7, 6)
        ]
        
        # 垂直墙壁 (行, 列)
        vertical_walls = [
            # 0,1之间的垂直墙在第2,4,5,6行
            (2, 1), (4, 1), (5, 1), (6, 1),
            # 1,2之间的垂直墙在第1,2,6行
            (1, 2), (2, 2), (6, 2),
            # 2,3之间的垂直墙在第0,4,6,7行
            (0, 3), (4, 3), (6, 3), (7, 3),
            # 3,4之间的垂直墙在第2,4,5,7行
            (2, 4), (4, 4), (5, 4), (7, 4),
            # 4,5之间的垂直墙在第3,4,6行
            (3, 5), (4, 5), (6, 5),
            # 5,6之间的垂直墙在第1,3,4,7行（删除第5行）
            (1, 6), (3, 6), (4, 6), (7, 6),
            # 6,7之间的垂直墙在第0,2,3,4行
            (0, 7), (2, 7), (3, 7), (4, 7),
            # 6,7行之间的第1列和第6列加墙
            (6, 1)
        ]
        
        self.walls['horizontal'].extend(horizontal_walls)
        self.walls['vertical'].extend(vertical_walls)
    
    def save_as_original(self):
        """保存当前迷宫为原始迷宫"""
        self.original_walls = {
            'horizontal': self.walls['horizontal'].copy(),
            'vertical': self.walls['vertical'].copy()
        }
    
    def restore_original(self):
        """恢复到原始迷宫"""
        if self.original_walls:
            self.walls = {
                'horizontal': self.original_walls['horizontal'].copy(),
                'vertical': self.original_walls['vertical'].copy()
            }
            # 恢复显示特殊标记
            self.show_special_markers = True
    
    def generate_random_maze(self):
        """生成完全随机的8x8迷宫"""
        # 清空现有墙壁
        self.walls = {
            'horizontal': [],
            'vertical': []
        }
        
        # 添加边界墙壁
        self.add_boundary_walls()
        
        # 随机生成终点位置
        self.generate_random_goal()
        
        # 生成随机内部墙壁
        self.add_random_internal_walls()
        
        # 确保起点和终点连通
        self.ensure_connectivity()
    
    def generate_random_goal(self):
        """随机生成终点位置"""
        # 确保终点不与起点相同
        while True:
            # 随机选择终点位置（可以是四周或中间）
            goal_row = random.randint(0, MAZE_SIZE - 1)
            goal_col = random.randint(0, MAZE_SIZE - 1)
            
            # 如果终点不是起点，则设置
            if (goal_row, goal_col) != self.castle:
                self.goal = (goal_row, goal_col)
                break
    
    def generate_vex_official_maze(self):
        """生成VEX官方8x8迷宫"""
        # VEX官方8x8迷宫的标准墙壁布局
        # 水平墙壁 (行, 列)
        horizontal_walls = [
            # 第1行墙壁
            (1, 0), (1, 2), (1, 4), (1, 6),
            # 第2行墙壁
            (2, 1), (2, 3), (2, 5), (2, 7),
            # 第3行墙壁
            (3, 0), (3, 2), (3, 4), (3, 6),
            # 第4行墙壁
            (4, 1), (4, 3), (4, 5), (4, 7),
            # 第5行墙壁
            (5, 0), (5, 2), (5, 4), (5, 6),
            # 第6行墙壁
            (6, 1), (6, 3), (6, 5), (6, 7),
            # 第7行墙壁
            (7, 0), (7, 2), (7, 4), (7, 6)
        ]
        
        # 垂直墙壁 (行, 列)
        vertical_walls = [
            # 第1列墙壁
            (0, 1), (2, 1), (4, 1), (6, 1),
            # 第2列墙壁
            (1, 2), (3, 2), (5, 2), (7, 2),
            # 第3列墙壁
            (0, 3), (2, 3), (4, 3), (6, 3),
            # 第4列墙壁
            (1, 4), (3, 4), (5, 4), (7, 4),
            # 第5列墙壁
            (0, 5), (2, 5), (4, 5), (6, 5),
            # 第6列墙壁
            (1, 6), (3, 6), (5, 6), (7, 6),
            # 第7列墙壁
            (0, 7), (2, 7), (4, 7), (6, 7)
        ]
        
        self.walls['horizontal'].extend(horizontal_walls)
        self.walls['vertical'].extend(vertical_walls)
    
    def add_random_internal_walls(self):
        """添加随机内部墙壁"""
        # 随机生成水平墙壁
        for row in range(1, MAZE_SIZE):
            for col in range(MAZE_SIZE):
                if random.random() < 0.4:  # 40%概率添加墙壁
                    self.walls['horizontal'].append((row, col))
        
        # 随机生成垂直墙壁
        for row in range(MAZE_SIZE):
            for col in range(1, MAZE_SIZE):
                if random.random() < 0.4:  # 40%概率添加墙壁
                    self.walls['vertical'].append((row, col))
        
        # 确保起点和终点可达（移除阻挡的墙壁）
        self.ensure_connectivity()
        
        # 确保没有四面封死的墙
        self.prevent_dead_ends()
        
        # 不显示特殊标记（字母和数字）
        self.show_special_markers = False
    
    def prevent_dead_ends(self):
        """防止四面封死的墙，确保每个格子至少有一个方向可以移动"""
        # 检查每个内部格子
        for row in range(1, MAZE_SIZE - 1):
            for col in range(1, MAZE_SIZE - 1):
                # 检查当前格子是否四面都被封死
                if self.is_dead_end(row, col):
                    # 随机选择一个方向移除墙壁
                    self.remove_random_wall(row, col)
    
    def is_dead_end(self, row, col):
        """检查指定位置是否四面都被封死"""
        # 检查四个方向是否都有墙壁阻挡
        directions_blocked = 0
        
        # 检查上方
        if (row, col) in self.walls['horizontal']:
            directions_blocked += 1
        
        # 检查下方
        if (row + 1, col) in self.walls['horizontal']:
            directions_blocked += 1
        
        # 检查左方
        if (row, col) in self.walls['vertical']:
            directions_blocked += 1
        
        # 检查右方
        if (row, col + 1) in self.walls['vertical']:
            directions_blocked += 1
        
        # 如果四个方向都被阻挡，则是死胡同
        return directions_blocked == 4
    
    def remove_random_wall(self, row, col):
        """随机移除指定位置的一个墙壁"""
        walls_to_remove = []
        
        # 收集可以移除的墙壁
        if (row, col) in self.walls['horizontal']:
            walls_to_remove.append(('horizontal', (row, col)))
        
        if (row + 1, col) in self.walls['horizontal']:
            walls_to_remove.append(('horizontal', (row + 1, col)))
        
        if (row, col) in self.walls['vertical']:
            walls_to_remove.append(('vertical', (row, col)))
        
        if (row, col + 1) in self.walls['vertical']:
            walls_to_remove.append(('vertical', (row, col + 1)))
        
        # 随机选择一个墙壁移除
        if walls_to_remove:
            wall_type, wall_pos = random.choice(walls_to_remove)
            if wall_pos in self.walls[wall_type]:
                self.walls[wall_type].remove(wall_pos)
    
    def ensure_connectivity(self):
        """确保起点和终点连通"""
        # 使用BFS检查连通性
        from collections import deque
        
        start = self.castle
        goal = self.goal
        
        # 检查是否已经连通
        if self.is_connected(start, goal):
            return True
        
        # 如果不连通，使用更智能的路径创建方法
        self.create_guaranteed_path()
        
        # 再次检查连通性
        return self.is_connected(start, goal)
    
    def is_connected(self, start, goal):
        """检查两个点是否连通"""
        from collections import deque
        
        queue = deque([start])
        visited = set([start])
        
        while queue:
            current = queue.popleft()
            if current == goal:
                return True
            
            # 检查四个方向
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
            
            for direction in directions:
                new_pos = (current[0] + direction[0], current[1] + direction[1])
                
                if (0 <= new_pos[0] < MAZE_SIZE and 0 <= new_pos[1] < MAZE_SIZE and 
                    new_pos not in visited and self.is_valid_move_between(current, new_pos)):
                    visited.add(new_pos)
                    queue.append(new_pos)
        
        return False
    
    def create_guaranteed_path(self):
        """创建一条保证连通的路径"""
        start_row, start_col = self.castle
        goal_row, goal_col = self.goal
        
        # 使用L形路径：先水平移动，再垂直移动
        # 或者先垂直移动，再水平移动
        
        # 方案1：先水平后垂直
        self.create_l_path_horizontal_first(start_row, start_col, goal_row, goal_col)
        
        # 如果方案1失败，尝试方案2：先垂直后水平
        if not self.is_connected(self.castle, self.goal):
            self.create_l_path_vertical_first(start_row, start_col, goal_row, goal_col)
    
    def create_l_path_horizontal_first(self, start_row, start_col, goal_row, goal_col):
        """创建L形路径：先水平移动，再垂直移动"""
        # 第一步：水平移动到目标列
        if start_col != goal_col:
            for col in range(min(start_col, goal_col), max(start_col, goal_col)):
                wall_to_remove = (start_row, col + 1)
                if wall_to_remove in self.walls['vertical']:
                    self.walls['vertical'].remove(wall_to_remove)
        
        # 第二步：垂直移动到目标行
        if start_row != goal_row:
            for row in range(min(start_row, goal_row), max(start_row, goal_row)):
                wall_to_remove = (row + 1, goal_col)
                if wall_to_remove in self.walls['horizontal']:
                    self.walls['horizontal'].remove(wall_to_remove)
    
    def create_l_path_vertical_first(self, start_row, start_col, goal_row, goal_col):
        """创建L形路径：先垂直移动，再水平移动"""
        # 第一步：垂直移动到目标行
        if start_row != goal_row:
            for row in range(min(start_row, goal_row), max(start_row, goal_row)):
                wall_to_remove = (row + 1, start_col)
                if wall_to_remove in self.walls['horizontal']:
                    self.walls['horizontal'].remove(wall_to_remove)
        
        # 第二步：水平移动到目标列
        if start_col != goal_col:
            for col in range(min(start_col, goal_col), max(start_col, goal_col)):
                wall_to_remove = (goal_row, col + 1)
                if wall_to_remove in self.walls['vertical']:
                    self.walls['vertical'].remove(wall_to_remove)
    
    
    def is_valid_move_between(self, from_pos, to_pos):
        """检查两个位置之间是否可以移动"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if from_row == to_row:  # 水平移动
            if from_col < to_col:  # 向右移动
                return (to_row, to_col) not in self.walls['vertical']
            else:  # 向左移动
                return (to_row, from_col) not in self.walls['vertical']
        elif from_col == to_col:  # 垂直移动
            if from_row < to_row:  # 向下移动
                return (to_row, to_col) not in self.walls['horizontal']
            else:  # 向上移动
                return (from_row, to_col) not in self.walls['horizontal']
        
        return False
    
    
    def draw(self, screen, robot):
        """绘制魔方迷宫"""
        # 绘制所有格子为白色通路
        for i in range(MAZE_SIZE):
            for j in range(MAZE_SIZE):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
        
        # 绘制网格线
        for i in range(MAZE_SIZE + 1):
            pygame.draw.line(screen, GRAY, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), 1)
        for j in range(MAZE_SIZE + 1):
            pygame.draw.line(screen, GRAY, (j * CELL_SIZE, 0), (j * CELL_SIZE, WINDOW_HEIGHT), 1)
        
        # 绘制墙壁线条
        self.draw_walls(screen)
        
        # 绘制特殊标记点
        self.draw_special_markers(screen)
        
        # 绘制机器人
        self.draw_robot(screen, robot)
    
    def draw_walls(self, screen):
        """绘制黑色墙壁线条"""
        # 绘制水平墙壁
        for wall in self.walls['horizontal']:
            x = wall[1] * CELL_SIZE
            y = wall[0] * CELL_SIZE
            # 判断是否为边界墙壁，加粗显示
            thickness = 5 if (wall[0] == 0 or wall[0] == MAZE_SIZE) else 3
            pygame.draw.line(screen, BLACK, (x, y), (x + CELL_SIZE, y), thickness)
        
        # 绘制垂直墙壁
        for wall in self.walls['vertical']:
            x = wall[1] * CELL_SIZE
            y = wall[0] * CELL_SIZE
            # 判断是否为边界墙壁，加粗显示
            thickness = 5 if (wall[1] == 0 or wall[1] == MAZE_SIZE) else 3
            pygame.draw.line(screen, BLACK, (x, y), (x, y + CELL_SIZE), thickness)
    
    def draw_special_markers(self, screen):
        """绘制所有特殊标记点"""
        # 绘制城堡（起点）
        castle_x = self.castle[1] * CELL_SIZE
        castle_y = self.castle[0] * CELL_SIZE
        pygame.draw.rect(screen, DARK_GREEN, (castle_x + 5, castle_y + 5, CELL_SIZE - 10, CELL_SIZE - 10))
        # 绘制城堡顶部
        pygame.draw.polygon(screen, GRAY, [
            (castle_x + CELL_SIZE//2, castle_y + 5),
            (castle_x + 10, castle_y + 20),
            (castle_x + CELL_SIZE - 10, castle_y + 20)
        ])
        
        # 绘制红黑相间的终点方块
        goal_x = self.goal[1] * CELL_SIZE
        goal_y = self.goal[0] * CELL_SIZE
        # 绘制棋盘格图案（适中大小，不压到黑墙）
        square_size = CELL_SIZE // 5  # 适中的方块大小
        margin = CELL_SIZE // 8  # 较小的边距
        for i in range(4):
            for j in range(4):
                if (i + j) % 2 == 0:
                    pygame.draw.rect(screen, RED, 
                        (goal_x + margin + j * square_size, goal_y + margin + i * square_size, 
                         square_size, square_size))
                else:
                    pygame.draw.rect(screen, BLACK, 
                        (goal_x + margin + j * square_size, goal_y + margin + i * square_size, 
                         square_size, square_size))
        
        # 绘制数字方块
        if self.show_special_markers:
            for num, pos in self.numbered_squares.items():
                x = pos[1] * CELL_SIZE
                y = pos[0] * CELL_SIZE
                pygame.draw.rect(screen, GREEN, (x + 5, y + 5, CELL_SIZE - 10, CELL_SIZE - 10))
                try:
                    font = pygame.font.SysFont('simhei', 36)
                except:
                    font = pygame.font.Font(None, 36)
                text = font.render(str(num), True, WHITE)
                text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
                screen.blit(text, text_rect)
        
        # 绘制字母圆圈
        if self.show_special_markers:
            for letter, pos in self.lettered_circles.items():
                x = pos[1] * CELL_SIZE + CELL_SIZE // 2
                y = pos[0] * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.circle(screen, LIGHT_BLUE, (x, y), CELL_SIZE // 3)
                try:
                    font = pygame.font.SysFont('simhei', 36)
                except:
                    font = pygame.font.Font(None, 36)
                text = font.render(letter, True, WHITE)
                text_rect = text.get_rect(center=(x, y))
                screen.blit(text, text_rect)
    
    def draw_robot(self, screen, robot):
        """绘制Arduino小车"""
        robot_x = robot.position[1] * CELL_SIZE + CELL_SIZE // 2
        robot_y = robot.position[0] * CELL_SIZE + CELL_SIZE // 2
        
        # Arduino小车的基本形状（向上方向）
        car_width = CELL_SIZE // 2.5
        car_height = CELL_SIZE // 3
        
        # 基础小车形状（相对于中心）
        base_points = [
            # 车身主体（矩形）
            (-car_width//2, -car_height//2),  # 左上
            (car_width//2, -car_height//2),   # 右上
            (car_width//2, car_height//2),    # 右下
            (-car_width//2, car_height//2),   # 左下
        ]
        
        # 车头指示器（小三角形）
        front_indicator = [
            (0, -car_height//2 - 5),          # 前方
            (-5, -car_height//2),            # 左前
            (5, -car_height//2),             # 右前
        ]
        
        # 计算当前角度
        base_angle = robot.direction * 90  # 基础角度：0=0°, 1=90°, 2=180°, 3=270°
        
        # 如果有转向动画，添加旋转效果
        if robot.turning:
            # 计算旋转进度（0-1）
            rotation_progress = robot.turn_progress / 30.0
            
            # 计算旋转角度（90度）
            rotation_angle = rotation_progress * 90
            
            if robot.turn_direction == 'left':
                rotation_angle = -rotation_angle  # 左转为负角度
            
            # 最终角度 = 基础角度 + 旋转角度
            final_angle = base_angle + rotation_angle
        else:
            final_angle = base_angle
        
        # 将角度转换为弧度
        angle_rad = math.radians(final_angle)
        
        # 旋转函数
        def rotate_point(x, y, angle_rad):
            rotated_x = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            rotated_y = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            return robot_x + rotated_x, robot_y + rotated_y
        
        # 旋转车身
        rotated_body = []
        for x, y in base_points:
            final_x, final_y = rotate_point(x, y, angle_rad)
            rotated_body.append((final_x, final_y))
        
        # 旋转车头指示器
        rotated_front = []
        for x, y in front_indicator:
            final_x, final_y = rotate_point(x, y, angle_rad)
            rotated_front.append((final_x, final_y))
        
        # 绘制Arduino小车车身（蓝色）
        pygame.draw.polygon(screen, BLUE, rotated_body)
        pygame.draw.polygon(screen, BLACK, rotated_body, 2)
        
        # 绘制车头指示器（红色）
        pygame.draw.polygon(screen, RED, rotated_front)
        
        # 绘制Arduino板细节
        # 绘制一些小的矩形代表Arduino的引脚
        pin_size = 2
        for i in range(3):
            for j in range(2):
                pin_x = robot_x - car_width//4 + i * car_width//6
                pin_y = robot_y - car_height//4 + j * car_height//2
                pin_final_x, pin_final_y = rotate_point(pin_x - robot_x, pin_y - robot_y, angle_rad)
                pygame.draw.rect(screen, WHITE, (pin_final_x - pin_size//2, pin_final_y - pin_size//2, pin_size, pin_size))
        
        # 绘制传感器
        self.draw_sensors(screen, robot, robot_x, robot_y)
        
        # 绘制转向指示
        if robot.turning:
            try:
                font = pygame.font.SysFont('simhei', 20)
            except:
                font = pygame.font.Font(None, 20)
            
            turn_text = font.render(f"转向中: {robot.turn_direction}", True, RED)
            screen.blit(turn_text, (robot_x - 40, robot_y - 50))
            
            # 绘制转向进度条
            progress_width = 60
            progress_height = 8
            progress_x = robot_x - progress_width // 2
            progress_y = robot_y - 30
            
            # 背景
            pygame.draw.rect(screen, GRAY, (progress_x, progress_y, progress_width, progress_height))
            # 进度
            progress_fill = int((robot.turn_progress / 30.0) * progress_width)
            pygame.draw.rect(screen, GREEN, (progress_x, progress_y, progress_fill, progress_height))
    
    def draw_sensors(self, screen, robot, robot_x, robot_y):
        """绘制超声波传感器"""
        sensor_length = CELL_SIZE // 2
        
        # 获取传感器距离
        front_distance = robot.get_sensor_distance('front')
        left_distance = robot.get_sensor_distance('left')
        right_distance = robot.get_sensor_distance('right')
        
        # 前方传感器
        front_sensor = robot.get_sensor_position('front')
        if front_sensor:
            color = RED if front_distance > 0 else GRAY
            pygame.draw.line(screen, color, (robot_x, robot_y), 
                           (front_sensor[1] * CELL_SIZE + CELL_SIZE // 2, 
                            front_sensor[0] * CELL_SIZE + CELL_SIZE // 2), 3)
            # 显示距离
            try:
                font = pygame.font.SysFont('simhei', 12)
            except:
                font = pygame.font.Font(None, 12)
            distance_text = font.render(f"F:{front_distance}", True, color)
            screen.blit(distance_text, (robot_x + 10, robot_y - 20))
        
        # 左方传感器
        left_sensor = robot.get_sensor_position('left')
        if left_sensor:
            color = GREEN if left_distance > 0 else GRAY
            pygame.draw.line(screen, color, (robot_x, robot_y), 
                           (left_sensor[1] * CELL_SIZE + CELL_SIZE // 2, 
                            left_sensor[0] * CELL_SIZE + CELL_SIZE // 2), 3)
            # 显示距离
            try:
                font = pygame.font.SysFont('simhei', 12)
            except:
                font = pygame.font.Font(None, 12)
            distance_text = font.render(f"L:{left_distance}", True, color)
            screen.blit(distance_text, (robot_x - 30, robot_y))
        
        # 右方传感器
        right_sensor = robot.get_sensor_position('right')
        if right_sensor:
            color = YELLOW if right_distance > 0 else GRAY
            pygame.draw.line(screen, color, (robot_x, robot_y), 
                           (right_sensor[1] * CELL_SIZE + CELL_SIZE // 2, 
                            right_sensor[0] * CELL_SIZE + CELL_SIZE // 2), 3)
            # 显示距离
            try:
                font = pygame.font.SysFont('simhei', 12)
            except:
                font = pygame.font.Font(None, 12)
            distance_text = font.render(f"R:{right_distance}", True, color)
            screen.blit(distance_text, (robot_x + 10, robot_y + 10))
    

class Robot:
    def __init__(self, maze):
        self.maze = maze
        self.position = maze.robot_pos  # 机器人初始位置在城堡附近
        self.direction = 0  # 方向：0=上，1=右，2=下，3=左
        self.path = []  # DFS路径
        self.dfs_path = []  # 保存的完整DFS路径
        self.visited = set()  # 已访问的位置
        self.dfs_complete = False  # DFS是否完成
        self.current_step = 0  # 当前步骤
        self.start_time = None  # 开始时间
        self.end_time = None  # 结束时间
        self.is_running = False  # 是否正在运行DFS
        self.turning = False  # 是否正在转向
        self.turn_direction = None  # 转向方向
        self.turn_progress = 0  # 转向进度
        self.pending_move = False  # 转向完成后是否需要移动
    
    def get_position(self):
        return self.position
    
    def set_position(self, pos):
        self.position = pos
    
    def get_sensor_distance(self, sensor_type):
        """获取超声波传感器距离（返回距离值，0表示有障碍物，>0表示距离）"""
        row, col = self.position
        
        if sensor_type == 'front':
            if self.direction == 0:  # 向上
                target_pos = (row - 1, col) if row > 0 else None
            elif self.direction == 1:  # 向右
                target_pos = (row, col + 1) if col < MAZE_SIZE - 1 else None
            elif self.direction == 2:  # 向下
                target_pos = (row + 1, col) if row < MAZE_SIZE - 1 else None
            else:  # 向左
                target_pos = (row, col - 1) if col > 0 else None
        
        elif sensor_type == 'left':
            if self.direction == 0:  # 向上
                target_pos = (row, col - 1) if col > 0 else None
            elif self.direction == 1:  # 向右
                target_pos = (row - 1, col) if row > 0 else None
            elif self.direction == 2:  # 向下
                target_pos = (row, col + 1) if col < MAZE_SIZE - 1 else None
            else:  # 向左
                target_pos = (row + 1, col) if row < MAZE_SIZE - 1 else None
        
        elif sensor_type == 'right':
            if self.direction == 0:  # 向上
                target_pos = (row, col + 1) if col < MAZE_SIZE - 1 else None
            elif self.direction == 1:  # 向右
                target_pos = (row + 1, col) if row < MAZE_SIZE - 1 else None
            elif self.direction == 2:  # 向下
                target_pos = (row, col - 1) if col > 0 else None
            else:  # 向左
                target_pos = (row - 1, col) if row > 0 else None
        else:
            return 0
        
        if target_pos is None:
            return 0  # 边界外，有障碍物
        
        # 检查是否有墙壁阻挡
        if not self.is_valid_move(target_pos):
            return 0  # 有墙壁，距离为0
        
        return 1  # 无障碍物，距离为1（一个格子）
    
    def get_sensor_position(self, sensor_type):
        """获取传感器检测位置（用于可视化）"""
        row, col = self.position
        
        if sensor_type == 'front':
            if self.direction == 0:  # 向上
                return (row - 1, col) if row > 0 else None
            elif self.direction == 1:  # 向右
                return (row, col + 1) if col < MAZE_SIZE - 1 else None
            elif self.direction == 2:  # 向下
                return (row + 1, col) if row < MAZE_SIZE - 1 else None
            else:  # 向左
                return (row, col - 1) if col > 0 else None
        
        elif sensor_type == 'left':
            if self.direction == 0:  # 向上
                return (row, col - 1) if col > 0 else None
            elif self.direction == 1:  # 向右
                return (row - 1, col) if row > 0 else None
            elif self.direction == 2:  # 向下
                return (row, col + 1) if col < MAZE_SIZE - 1 else None
            else:  # 向左
                return (row + 1, col) if row < MAZE_SIZE - 1 else None
        
        elif sensor_type == 'right':
            if self.direction == 0:  # 向上
                return (row, col + 1) if col < MAZE_SIZE - 1 else None
            elif self.direction == 1:  # 向右
                return (row + 1, col) if row < MAZE_SIZE - 1 else None
            elif self.direction == 2:  # 向下
                return (row, col - 1) if col > 0 else None
            else:  # 向左
                return (row - 1, col) if row > 0 else None
        
        return None
    
    def turn_left(self, use_animation=True):
        """左转"""
        old_direction = self.direction
        self.direction = (self.direction - 1) % 4
        
        if use_animation:
            self.turning = True
            self.turn_direction = 'left'
            self.turn_progress = 0
        else:
            self.turning = False
            self.turn_direction = None
            self.turn_progress = 0
            
        print(f"左转: {old_direction} -> {self.direction}")
    
    def turn_right(self, use_animation=True):
        """右转"""
        old_direction = self.direction
        self.direction = (self.direction + 1) % 4
        
        if use_animation:
            self.turning = True
            self.turn_direction = 'right'
            self.turn_progress = 0
        else:
            self.turning = False
            self.turn_direction = None
            self.turn_progress = 0
            
        print(f"右转: {old_direction} -> {self.direction}")
    
    def update_turning_animation(self):
        """更新转向动画"""
        if self.turning:
            self.turn_progress += 1
            if self.turn_progress >= 30:  # 转向动画持续30帧，让90度旋转更平滑
                self.turning = False
                self.turn_direction = None
                self.turn_progress = 0
    
    def move_forward(self):
        """向前移动"""
        # 根据当前方向计算前进位置
        row, col = self.position
        
        if self.direction == 0:  # 向上
            new_pos = (row - 1, col)
        elif self.direction == 1:  # 向右
            new_pos = (row, col + 1)
        elif self.direction == 2:  # 向下
            new_pos = (row + 1, col)
        else:  # 向左
            new_pos = (row, col - 1)
        
        if self.is_valid_move(new_pos):
            self.position = new_pos
            return True
        return False
    
    def reset_dfs(self):
        """重置DFS状态"""
        self.path = []
        self.dfs_path = []
        self.visited = set()
        self.dfs_complete = False
        self.current_step = 0
        self.start_time = None
        self.end_time = None
        self.is_running = False
        self.position = self.maze.robot_pos  # 重置到起点
        self.direction = 0  # 重置方向
        self.turning = False
        self.turn_direction = None
        self.turn_progress = 0
        self.pending_move = False
        # 重置DFS专用状态
        self.dfs_stack = []
        self.dfs_visited = set()
        self.dfs_target = None
        self.dfs_moving_to_target = False
        # 重置BFS专用状态
        self.bfs_queue = []
        self.bfs_visited = set()
        self.bfs_target = None
        self.bfs_moving_to_target = False
        # 重置Greedy专用状态
        self.greedy_visited = set()
        self.greedy_path = []
        self.greedy_target = None
        self.greedy_moving_to_target = False
    
    def is_valid_move(self, pos):
        """检查移动是否有效（不撞墙）"""
        row, col = pos
        if row < 0 or row >= MAZE_SIZE or col < 0 or col >= MAZE_SIZE:
            return False
        
        # 检查垂直墙壁
        current_row, current_col = self.position
        if current_row == row:  # 水平移动
            if current_col < col:  # 向右移动
                if (row, col) in self.maze.walls['vertical']:
                    return False
            else:  # 向左移动
                if (row, current_col) in self.maze.walls['vertical']:
                    return False
        elif current_col == col:  # 垂直移动
            if current_row < row:  # 向下移动
                if (row, col) in self.maze.walls['horizontal']:
                    return False
            else:  # 向上移动
                if (current_row, col) in self.maze.walls['horizontal']:
                    return False
        
        return True
    
    def dfs_search(self):
        """执行深度优先搜索算法（DFS）- 简化版本"""
        if self.dfs_complete:
            return
        
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
            # 初始化DFS状态
            self.dfs_stack = [self.position]  # 只存储位置
            self.dfs_visited = {self.position}
            self.dfs_path = []
            self.dfs_target = None
            self.dfs_moving_to_target = False
        
        # 如果到达终点
        if self.position == self.maze.goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            self.dfs_path = self.path.copy()
            return
        
        # 如果正在移动到目标位置
        if self.dfs_moving_to_target and self.dfs_target:
            if self.position == self.dfs_target:
                # 到达目标位置
                self.dfs_moving_to_target = False
                self.dfs_target = None
                # 继续DFS探索
                self.continue_dfs_exploration()
            else:
                # 继续移动到目标位置
                self.move_towards_target(self.dfs_target)
            return
        
        # 如果栈为空，没有找到路径
        if not self.dfs_stack:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            return
        
        # 开始新的探索
        self.continue_dfs_exploration()
    
    def continue_dfs_exploration(self):
        """继续DFS探索过程 - 简化版本"""
        if not self.dfs_stack:
            return
        
        # 获取当前位置
        current = self.position
        
        # 四个方向 (上, 下, 左, 右)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        current_row, current_col = current
        
        # 寻找第一个未访问的邻居
        for dr, dc in directions:
            nr, nc = current_row + dr, current_col + dc
            if (0 <= nr < MAZE_SIZE and 0 <= nc < MAZE_SIZE):  # 边界检查
                if self.is_valid_move_from_to(current, (nr, nc)) and (nr, nc) not in self.dfs_visited:
                    # 找到未访问的邻居，移动到该位置
                    self.dfs_visited.add((nr, nc))
                    self.dfs_target = (nr, nc)
                    self.dfs_moving_to_target = True
                    # 开始移动到目标位置
                    self.move_towards_target((nr, nc))
                    return
        
        # 没有找到未访问的邻居，需要回溯
        if len(self.path) > 1:
            # 回溯到上一个位置
            prev_position = self.path[-2]  # 上一个位置
            self.dfs_target = prev_position
            self.dfs_moving_to_target = True
            # 从路径中移除当前位置
            self.path.pop()
            # 开始回溯移动
            self.move_towards_target(prev_position)
        else:
            # 没有更多位置可探索，DFS完成
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
    
    def move_towards_target(self, target):
        """移动到目标位置"""
        current_row, current_col = self.position
        target_row, target_col = target
        
        # 计算需要移动的方向
        if target_row < current_row:  # 需要向上
            target_direction = 0
        elif target_row > current_row:  # 需要向下
            target_direction = 2
        elif target_col < current_col:  # 需要向左
            target_direction = 3
        elif target_col > current_col:  # 需要向右
            target_direction = 1
        else:
            # 已经在目标位置
            return
        
        # 如果当前方向不正确，先转向
        if self.direction != target_direction:
            self.turn_to_direction(target_direction)
            return
        
        # 方向正确，尝试前进
        if self.move_forward():
            self.path.append(self.position)
            self.current_step += 1
        else:
            # 无法前进，可能路径被阻塞
            self.dfs_moving_to_target = False
            self.dfs_target = None
    
    def turn_to_direction(self, target_direction):
        """转向到指定方向"""
        # 计算需要转向的次数
        turns_needed = (target_direction - self.direction) % 4
        
        if turns_needed == 1:
            self.turn_right()
        elif turns_needed == 2:
            # 选择最短路径：右转2次或左转2次
            self.turn_right()
        elif turns_needed == 3:
            self.turn_left()
    
    def get_neighbors(self, position):
        """获取指定位置的所有邻居"""
        row, col = position
        neighbors = []
        
        # 四个方向的邻居
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
        
        for direction in directions:
            neighbor_row = row + direction[0]
            neighbor_col = col + direction[1]
            
            # 检查是否在迷宫范围内
            if (0 <= neighbor_row < MAZE_SIZE and 0 <= neighbor_col < MAZE_SIZE):
                neighbors.append((neighbor_row, neighbor_col))
        
        return neighbors
    
    def bfs_search(self):
        """执行广度优先搜索算法（BFS）- 模仿DFS工作方式"""
        if self.dfs_complete:
            return
        
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
            # 初始化BFS状态
            self.bfs_queue = [self.position]  # 只存储位置
            self.bfs_visited = {self.position}
            self.bfs_path = []
            self.bfs_target = None
            self.bfs_moving_to_target = False
        
        # 如果到达终点
        if self.position == self.maze.goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            self.dfs_path = self.path.copy()
            return
        
        # 如果正在移动到目标位置
        if self.bfs_moving_to_target and self.bfs_target:
            if self.position == self.bfs_target:
                # 到达目标位置
                self.bfs_moving_to_target = False
                self.bfs_target = None
                # 继续BFS探索
                self.continue_bfs_exploration()
            else:
                # 继续移动到目标位置
                self.move_towards_target(self.bfs_target)
            return
        
        # 如果队列为空，没有找到路径
        if not self.bfs_queue:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            return
        
        # 开始新的探索
        self.continue_bfs_exploration()
    
    def continue_bfs_exploration(self):
        """继续BFS探索过程 - 模仿DFS工作方式"""
        if not self.bfs_queue:
            return
        
        # 获取当前位置
        current = self.position
        
        # 四个方向 (上, 下, 左, 右)
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        current_row, current_col = current
        
        # 寻找第一个未访问的邻居
        for dr, dc in directions:
            nr, nc = current_row + dr, current_col + dc
            if (0 <= nr < MAZE_SIZE and 0 <= nc < MAZE_SIZE):  # 边界检查
                if self.is_valid_move_from_to(current, (nr, nc)) and (nr, nc) not in self.bfs_visited:
                    # 找到未访问的邻居，移动到该位置
                    self.bfs_visited.add((nr, nc))
                    self.bfs_target = (nr, nc)
                    self.bfs_moving_to_target = True
                    # 开始移动到目标位置
                    self.move_towards_target((nr, nc))
                    return
        
        # 没有找到未访问的邻居，需要回溯
        if len(self.path) > 1:
            # 回溯到上一个位置
            prev_position = self.path[-2]  # 上一个位置
            self.bfs_target = prev_position
            self.bfs_moving_to_target = True
            # 从路径中移除当前位置
            self.path.pop()
            # 开始回溯移动
            self.move_towards_target(prev_position)
        else:
            # 没有更多位置可探索，BFS完成
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
    
    def reconstruct_path(self, parent, start, goal):
        """重构从起点到终点的路径"""
        path = []
        current = goal
        
        while current != start:
            path.append(current)
            current = parent.get(current)
            if current is None:
                return None  # 无法重构路径
        
        path.append(start)
        path.reverse()
        return path
    
    def greedy_search(self):
        """执行改进的贪心搜索算法（最佳优先搜索）"""
        if self.dfs_complete:
            return
        
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
            # 初始化贪心搜索专用状态
            self.greedy_visited = set()
            self.greedy_path = []
            self.greedy_target = None
            self.greedy_moving_to_target = False
        
        # 如果到达终点
        if self.position == self.maze.goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            self.dfs_path = self.path.copy()
            return
        
        # 如果正在移动到目标位置
        if self.greedy_moving_to_target and self.greedy_target:
            if self.position == self.greedy_target:
                # 到达目标位置
                self.greedy_moving_to_target = False
                self.greedy_target = None
                # 继续贪心探索
                self.continue_greedy_exploration()
            else:
                # 继续移动到目标位置
                self.move_towards_target(self.greedy_target)
            return
        
        # 开始新的贪心探索
        self.continue_greedy_exploration()
    
    def continue_greedy_exploration(self):
        """继续贪心探索过程"""
        # 标记当前位置为已访问
        self.greedy_visited.add(self.position)
        
        # 改进的启发式函数：结合曼哈顿距离和路径质量
        def enhanced_heuristic(pos):
            """增强的启发式函数"""
            # 基础曼哈顿距离
            manhattan_dist = abs(pos[0] - self.maze.goal[0]) + abs(pos[1] - self.maze.goal[1])
            
            # 路径质量评估：检查该位置是否会导致死胡同
            dead_end_penalty = calculate_dead_end_penalty(pos)
            
            # 方向偏好：优先选择朝向目标的方向
            direction_bonus = calculate_direction_bonus(pos)
            
            # 综合评估
            return manhattan_dist + dead_end_penalty - direction_bonus
        
        def calculate_dead_end_penalty(pos):
            """计算死胡同惩罚"""
            # 检查该位置的邻居数量
            neighbors = self.get_valid_neighbors(pos)
            unvisited_neighbors = [n for n in neighbors if n not in self.greedy_visited]
            
            if len(unvisited_neighbors) == 0:
                return 10  # 死胡同，高惩罚
            elif len(unvisited_neighbors) == 1:
                return 5   # 只有一个选择，中等惩罚
            else:
                return 0   # 多个选择，无惩罚
        
        def calculate_direction_bonus(pos):
            """计算方向奖励"""
            current_row, current_col = self.position
            target_row, target_col = self.maze.goal
            
            # 计算朝向目标的方向
            row_diff = target_row - current_row
            col_diff = target_col - current_col
            
            # 检查移动是否朝向目标
            if row_diff != 0 and pos[0] == current_row + (1 if row_diff > 0 else -1):
                return 2  # 朝向目标的行方向
            elif col_diff != 0 and pos[1] == current_col + (1 if col_diff > 0 else -1):
                return 2  # 朝向目标的列方向
            else:
                return 0  # 不朝向目标
        
        # 获取所有可移动的邻居
        neighbors = self.get_valid_neighbors(self.position)
        unvisited_neighbors = [n for n in neighbors if n not in self.greedy_visited]
        
        if unvisited_neighbors:
            # 计算每个邻居的启发式值
            neighbor_scores = []
            for neighbor in unvisited_neighbors:
                score = enhanced_heuristic(neighbor)
                neighbor_scores.append((neighbor, score))
            
            # 选择最佳邻居
            best_neighbor = min(neighbor_scores, key=lambda x: x[1])
            self.greedy_target = best_neighbor[0]
            self.greedy_moving_to_target = True
            
            # 开始移动到目标位置
            self.move_towards_target(self.greedy_target)
        else:
            # 没有未访问的邻居，需要智能回溯
            self.smart_backtrack()
    
    def get_valid_neighbors(self, pos):
        """获取指定位置的所有有效邻居"""
        row, col = pos
        neighbors = []
        
        # 四个方向的邻居
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
        
        for direction in directions:
            neighbor_row = row + direction[0]
            neighbor_col = col + direction[1]
            
            # 检查是否在迷宫范围内且可以移动
            if (0 <= neighbor_row < MAZE_SIZE and 0 <= neighbor_col < MAZE_SIZE and 
                self.is_valid_move_from_to(pos, (neighbor_row, neighbor_col))):
                neighbors.append((neighbor_row, neighbor_col))
        
        return neighbors
    
    def smart_backtrack(self):
        """智能回溯：寻找最近的未访问区域"""
        # 从路径中寻找最近的未访问邻居
        for i in range(len(self.path) - 1, -1, -1):
            backtrack_pos = self.path[i]
            neighbors = self.get_valid_neighbors(backtrack_pos)
            unvisited_neighbors = [n for n in neighbors if n not in self.greedy_visited]
            
            if unvisited_neighbors:
                # 找到有未访问邻居的位置，回溯到那里
                self.greedy_target = backtrack_pos
                self.greedy_moving_to_target = True
                # 从路径中移除当前位置到回溯位置之间的所有位置
                self.path = self.path[:i+1]
                # 开始回溯移动
                self.move_towards_target(backtrack_pos)
                return
        
        # 如果所有位置都没有未访问的邻居，搜索完成
        self.dfs_complete = True
        self.end_time = pygame.time.get_ticks()
    
    def flood_filled_search(self):
        """执行洪水填充搜索算法（Flood Fill）"""
        if self.dfs_complete:
            return
        
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
        
        # 如果到达终点
        if self.position == self.maze.goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            self.dfs_path = self.path.copy()
            return
        
        # 洪水填充算法：从终点开始填充距离值
        if not hasattr(self, 'flood_map'):
            self.create_flood_map()
        
        # 标记当前位置为已访问
        self.visited.add(self.position)
        
        # 找到所有可移动的位置
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
        valid_moves = []
        
        for direction in directions:
            new_pos = (self.position[0] + direction[0], self.position[1] + direction[1])
            if (new_pos not in self.visited and 
                self.is_valid_move(new_pos) and 
                new_pos in self.flood_map):
                valid_moves.append((new_pos, self.flood_map[new_pos]))
        
        if valid_moves:
            # 选择洪水值最小的位置（离终点最近）
            best_move = min(valid_moves, key=lambda x: x[1])
            self.position = best_move[0]
            self.path.append(self.position)
            self.current_step += 1
        else:
            # 如果没有可移动的方向，回溯
            if self.path:
                self.path.pop()
                if self.path:
                    self.position = self.path[-1]
                else:
                    self.position = self.maze.robot_pos
                self.current_step += 1
            else:
                self.dfs_complete = True
                self.end_time = pygame.time.get_ticks()
    
    def create_flood_map(self):
        """创建洪水填充地图（从终点开始BFS填充距离值）"""
        from collections import deque
        
        self.flood_map = {}
        queue = deque([(self.maze.goal, 0)])
        visited = set([self.maze.goal])
        
        while queue:
            current, distance = queue.popleft()
            self.flood_map[current] = distance
            
            # 检查四个方向
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
            
            for direction in directions:
                new_pos = (current[0] + direction[0], current[1] + direction[1])
                
                if (new_pos not in visited and 
                    self.is_valid_move_from_to(current, new_pos)):
                    visited.add(new_pos)
                    queue.append((new_pos, distance + 1))
    
    def wall_follow_search(self, speed=5):
        """执行墙跟随搜索算法（标准右手法则）"""
        if self.dfs_complete:
            return
        
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
        
        # 如果到达终点
        if self.position == self.maze.goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            self.dfs_path = self.path.copy()
            return
        
        # 如果正在转向，等待转向完成
        if self.turning:
            return
        
        # 如果转向完成且有待移动，执行移动
        if self.pending_move:
            if self.move_forward():
                self.path.append(self.position)
                self.current_step += 1
            self.pending_move = False
            return
        
        # 标记当前位置为已访问
        self.visited.add(self.position)
        
        # 标准墙跟随算法：
        # while not at exit:
        #     if right is free:
        #         turn right
        #         move forward
        #     else if front is free:
        #         move forward
        #     else if left is free:
        #         turn left
        #         move forward
        #     else:
        #         turn around (180°)
        
        # 检查右侧是否空闲
        if self.is_right_free():
            use_animation = speed > 1  # 速度为1时不使用动画
            self.turn_right(use_animation)
            if not use_animation:
                # 不使用动画时，直接移动
                if self.move_forward():
                    self.path.append(self.position)
                    self.current_step += 1
            else:
                self.pending_move = True  # 转向完成后需要移动
            return  # 等待转向完成
        
        # 检查前方是否空闲
        elif self.is_front_free():
            if self.move_forward():
                self.path.append(self.position)
                self.current_step += 1
            return
        
        # 检查左侧是否空闲
        elif self.is_left_free():
            use_animation = speed > 1  # 速度为1时不使用动画
            self.turn_left(use_animation)
            if not use_animation:
                # 不使用动画时，直接移动
                if self.move_forward():
                    self.path.append(self.position)
                    self.current_step += 1
            else:
                self.pending_move = True  # 转向完成后需要移动
            return  # 等待转向完成
        
        # 都不空闲，掉头180度
        else:
            use_animation = speed > 1  # 速度为1时不使用动画
            self.turn_right(use_animation)  # 右转90度
            if not use_animation:
                # 不使用动画时，直接移动
                if self.move_forward():
                    self.path.append(self.position)
                    self.current_step += 1
            else:
                self.pending_move = True  # 转向完成后需要移动
            return  # 等待转向完成
    
    def is_right_free(self):
        """检查右侧是否空闲"""
        row, col = self.position
        
        if self.direction == 0:  # 向上
            right_pos = (row, col + 1)
        elif self.direction == 1:  # 向右
            right_pos = (row + 1, col)
        elif self.direction == 2:  # 向下
            right_pos = (row, col - 1)
        else:  # 向左
            right_pos = (row - 1, col)
        
        return self.is_valid_move(right_pos)
    
    def is_front_free(self):
        """检查前方是否空闲"""
        row, col = self.position
        
        if self.direction == 0:  # 向上
            front_pos = (row - 1, col)
        elif self.direction == 1:  # 向右
            front_pos = (row, col + 1)
        elif self.direction == 2:  # 向下
            front_pos = (row + 1, col)
        else:  # 向左
            front_pos = (row, col - 1)
        
        return self.is_valid_move(front_pos)
    
    def is_left_free(self):
        """检查左侧是否空闲"""
        row, col = self.position
        
        if self.direction == 0:  # 向上
            left_pos = (row, col - 1)
        elif self.direction == 1:  # 向右
            left_pos = (row - 1, col)
        elif self.direction == 2:  # 向下
            left_pos = (row, col + 1)
        else:  # 向左
            left_pos = (row + 1, col)
        
        return self.is_valid_move(left_pos)
    
    def astar_search(self):
        """执行A*搜索算法（A-Star）"""
        if self.dfs_complete:
            return
        
        if not self.is_running:
            self.start_time = pygame.time.get_ticks()
            self.is_running = True
        
        # 如果到达终点
        if self.position == self.maze.goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            self.dfs_path = self.path.copy()
            return
        
        # A*算法：f(n) = g(n) + h(n)
        # g(n): 从起点到n的实际距离
        # h(n): 从n到终点的启发式距离（曼哈顿距离）
        # f(n): 总评估函数
        import heapq
        
        start = self.position
        goal = self.maze.goal
        
        if start == goal:
            self.dfs_complete = True
            self.end_time = pygame.time.get_ticks()
            return
        
        # 启发式函数（曼哈顿距离）
        def heuristic(pos):
            return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])
        
        # 优先队列：(f_score, g_score, position, path)
        open_set = [(heuristic(start), 0, start, [start])]
        closed_set = set()
        
        while open_set:
            f_score, g_score, current, path = heapq.heappop(open_set)
            
            if current in closed_set:
                continue
            
            closed_set.add(current)
            
            if current == goal:
                # 找到最优路径，移动到下一个位置
                if len(path) > 1:
                    self.position = path[1]
                    self.path = path[1:]
                    self.visited.add(self.position)
                    self.current_step += 1
                else:
                    self.dfs_complete = True
                    self.end_time = pygame.time.get_ticks()
                return
            
            # 检查四个方向
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
            
            for direction in directions:
                new_pos = (current[0] + direction[0], current[1] + direction[1])
                
                if (new_pos not in closed_set and 
                    self.is_valid_move_from_to(current, new_pos)):
                    
                    new_g_score = g_score + 1
                    new_f_score = new_g_score + heuristic(new_pos)
                    new_path = path + [new_pos]
                    
                    heapq.heappush(open_set, (new_f_score, new_g_score, new_pos, new_path))
        
        # 如果没有找到路径，标记为完成
        self.dfs_complete = True
        self.end_time = pygame.time.get_ticks()
    
    def turn_to_target(self, target_pos):
        """转向到目标位置（逐步转向）"""
        current_row, current_col = self.position
        target_row, target_col = target_pos
        
        print(f"转向计算: 当前位置{self.position}, 目标位置{target_pos}, 当前方向{self.direction}")
        
        # 计算需要转向的方向
        if target_row < current_row:  # 需要向上
            target_direction = 0
        elif target_row > current_row:  # 需要向下
            target_direction = 2
        elif target_col < current_col:  # 需要向左
            target_direction = 3
        elif target_col > current_col:  # 需要向右
            target_direction = 1
        else:
            print("已经在目标位置")
            return  # 已经在目标位置
        
        # 计算转向次数（最多3次）
        turns_needed = (target_direction - self.direction) % 4
        
        print(f"需要转向到方向{target_direction}, 需要{turns_needed}次转向")
        
        # 只进行一次转向，让机器人逐步转向
        if turns_needed == 1:
            print("执行右转")
            self.turn_right()
        elif turns_needed == 2:
            # 选择最短路径：右转2次或左转2次，这里选择右转
            print("执行右转（还需要1次）")
            self.turn_right()
        elif turns_needed == 3:
            print("执行左转")
            self.turn_left()  # 左转更近
    
    
    def sensor_based_movement(self):
        """基于传感器信息的移动决策"""
        # 获取三个传感器的距离
        front_distance = self.get_sensor_distance('front')
        left_distance = self.get_sensor_distance('left')
        right_distance = self.get_sensor_distance('right')
        
        print(f"传感器读数: 前方={front_distance}, 左方={left_distance}, 右方={right_distance}")
        
        # 如果前方有路，优先直行
        if front_distance > 0:
            print("前方无障碍，直行")
            return self.move_forward()
        
        # 前方有障碍，需要转向
        if left_distance > 0 and right_distance > 0:
            # 左右都有路，优先左转（左转优先策略）
            print("前方有障碍，左右都有路，选择左转")
            self.turn_left()
            return False
        elif left_distance > 0:
            # 只有左边有路
            print("前方有障碍，只有左边有路，左转")
            self.turn_left()
            return False
        elif right_distance > 0:
            # 只有右边有路
            print("前方有障碍，只有右边有路，右转")
            self.turn_right()
            return False
        else:
            # 三个方向都有障碍，需要掉头
            print("三个方向都有障碍，掉头")
            self.turn_right()  # 右转两次等于掉头
            return False
    
    def move_to_goal_with_sensors(self):
        """使用传感器系统移动到终点"""
        if not self.dfs_complete or not self.dfs_path:
            print(f"DFS未完成或路径为空: dfs_complete={self.dfs_complete}, dfs_path长度={len(self.dfs_path)}")
            return False

        # 如果已经在终点
        if self.position == self.maze.goal:
            print("已到达终点")
            return True

        # 查看下一个目标格子
        target_pos = self.dfs_path[0]
        print(f"当前位置: {self.position}, 目标位置: {target_pos}, 当前方向: {self.direction}")

        # 使用传感器系统进行移动决策
        moved = self.sensor_based_movement()
        
        if moved:
            # 成功移动，检查是否到达了目标位置
            if self.position == target_pos:
                self.dfs_path.pop(0)  # 移除已走的格子
                print("到达目标位置")
            else:
                print("移动了但不是目标位置")
        
        return moved

    def facing_target(self, target_pos):
        """判断是否已经面向目标格子"""
        current_row, current_col = self.position
        target_row, target_col = target_pos

        if target_row < current_row and self.direction == 0:
            return True
        if target_row > current_row and self.direction == 2:
            return True
        if target_col < current_col and self.direction == 3:
            return True
        if target_col > current_col and self.direction == 1:
            return True
        return False
    
    def find_path_to_goal(self):
        """使用BFS找到从当前位置到终点的最短路径"""
        from collections import deque
        
        start = self.position
        goal = self.maze.goal
        
        if start == goal:
            return [start]
        
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            current, path = queue.popleft()
            
            # 检查四个方向
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 右、下、左、上
            
            for direction in directions:
                new_pos = (current[0] + direction[0], current[1] + direction[1])
                
                if new_pos == goal:
                    return path + [new_pos]
                
                if (new_pos not in visited and 
                    self.is_valid_move_from_to(current, new_pos)):
                    visited.add(new_pos)
                    queue.append((new_pos, path + [new_pos]))
        
        return None
    
    def is_valid_move_from_to(self, from_pos, to_pos):
        """检查从from_pos到to_pos的移动是否有效"""
        row, col = to_pos
        if row < 0 or row >= MAZE_SIZE or col < 0 or col >= MAZE_SIZE:
            return False
        
        # 检查垂直墙壁
        from_row, from_col = from_pos
        if from_row == row:  # 水平移动
            if from_col < col:  # 向右移动
                if (row, col) in self.maze.walls['vertical']:
                    return False
            else:  # 向左移动
                if (row, from_col) in self.maze.walls['vertical']:
                    return False
        elif from_col == col:  # 垂直移动
            if from_row < row:  # 向下移动
                if (row, col) in self.maze.walls['horizontal']:
                    return False
            else:  # 向上移动
                if (from_row, col) in self.maze.walls['horizontal']:
                    return False
        
        return True

# 滑动按钮相关变量
slider_x = WINDOW_WIDTH - 100
slider_y = 10
slider_width = 80
slider_height = 20
slider_handle_size = 20

def draw_speed_slider(screen, speed):
    """绘制速度调节滑动按钮"""
    # 绘制滑动条背景
    pygame.draw.rect(screen, GRAY, (slider_x, slider_y, slider_width, slider_height))
    
    # 计算滑块位置（速度范围：1-20）
    speed_normalized = (speed - 1) / 19.0
    handle_x = slider_x + int(speed_normalized * (slider_width - slider_handle_size))
    
    # 绘制滑块
    pygame.draw.rect(screen, BLUE, (handle_x, slider_y - 2, slider_handle_size, slider_height + 4))
    
    # 绘制速度文字
    try:
        font = pygame.font.SysFont('simhei', 16)
    except:
        font = pygame.font.Font(None, 16)
    
    speed_text = font.render(f"速度: {speed}", True, BLACK)
    screen.blit(speed_text, (slider_x, slider_y - 25))

def handle_slider_click(mouse_pos):
    """处理滑动按钮点击"""
    mouse_x, mouse_y = mouse_pos
    
    if (slider_x <= mouse_x <= slider_x + slider_width and 
        slider_y <= mouse_y <= slider_y + slider_height):
        # 计算新的速度值
        relative_x = mouse_x - slider_x
        speed_normalized = relative_x / slider_width
        new_speed = int(speed_normalized * 19) + 1
        return max(1, min(20, new_speed))  # 限制在1-20范围内
    
    return None

# Reset按钮相关变量
reset_button_x = WINDOW_WIDTH - 100
reset_button_y = 50
reset_button_width = 80
reset_button_height = 30

# Shuffle按钮相关变量
shuffle_button_x = WINDOW_WIDTH - 100
shuffle_button_y = 90
shuffle_button_width = 80
shuffle_button_height = 30

# Origin按钮相关变量
origin_button_x = WINDOW_WIDTH - 100
origin_button_y = 130
origin_button_width = 80
origin_button_height = 30

# Wall-following按钮相关变量
wall_following_button_x = WINDOW_WIDTH - 160
wall_following_button_y = 170
wall_following_button_width = 150
wall_following_button_height = 30
dropdown_open = False
current_algorithm = "Wall-follow"
algorithms = ["Wall-follow", "Greedy", "DFS", "BFS", "Flood-filled", "A*"]

def draw_reset_button(screen):
    """绘制Reset按钮"""
    # 绘制按钮背景
    pygame.draw.rect(screen, RED, (reset_button_x, reset_button_y, reset_button_width, reset_button_height))
    
    # 绘制按钮边框
    pygame.draw.rect(screen, BLACK, (reset_button_x, reset_button_y, reset_button_width, reset_button_height), 2)
    
    # 绘制按钮文字
    try:
        font = pygame.font.SysFont('simhei', 16)
    except:
        font = pygame.font.Font(None, 16)
    
    reset_text = font.render("Reset", True, WHITE)
    text_rect = reset_text.get_rect(center=(reset_button_x + reset_button_width//2, reset_button_y + reset_button_height//2))
    screen.blit(reset_text, text_rect)

def handle_reset_button_click(mouse_pos):
    """处理Reset按钮点击"""
    mouse_x, mouse_y = mouse_pos
    
    if (reset_button_x <= mouse_x <= reset_button_x + reset_button_width and 
        reset_button_y <= mouse_y <= reset_button_y + reset_button_height):
        return True
    
    return False

def draw_shuffle_button(screen):
    """绘制Shuffle按钮"""
    # 绘制按钮背景
    pygame.draw.rect(screen, GREEN, (shuffle_button_x, shuffle_button_y, shuffle_button_width, shuffle_button_height))
    
    # 绘制按钮边框
    pygame.draw.rect(screen, BLACK, (shuffle_button_x, shuffle_button_y, shuffle_button_width, shuffle_button_height), 2)
    
    # 绘制按钮文字
    try:
        font = pygame.font.SysFont('simhei', 16)
    except:
        font = pygame.font.Font(None, 16)
    
    shuffle_text = font.render("Shuffle", True, WHITE)
    text_rect = shuffle_text.get_rect(center=(shuffle_button_x + shuffle_button_width//2, shuffle_button_y + shuffle_button_height//2))
    screen.blit(shuffle_text, text_rect)

def handle_shuffle_button_click(mouse_pos):
    """处理Shuffle按钮点击"""
    mouse_x, mouse_y = mouse_pos
    
    if (shuffle_button_x <= mouse_x <= shuffle_button_x + shuffle_button_width and 
        shuffle_button_y <= mouse_y <= shuffle_button_y + shuffle_button_height):
        return True
    
    return False

def draw_origin_button(screen):
    """绘制Origin按钮"""
    # 绘制按钮背景
    pygame.draw.rect(screen, BLUE, (origin_button_x, origin_button_y, origin_button_width, origin_button_height))
    
    # 绘制按钮边框
    pygame.draw.rect(screen, BLACK, (origin_button_x, origin_button_y, origin_button_width, origin_button_height), 2)
    
    # 绘制按钮文字
    try:
        font = pygame.font.SysFont('simhei', 16)
    except:
        font = pygame.font.Font(None, 16)
    
    origin_text = font.render("Origin", True, WHITE)
    text_rect = origin_text.get_rect(center=(origin_button_x + origin_button_width//2, origin_button_y + origin_button_height//2))
    screen.blit(origin_text, text_rect)

def handle_origin_button_click(mouse_pos):
    """处理Origin按钮点击"""
    mouse_x, mouse_y = mouse_pos
    
    if (origin_button_x <= mouse_x <= origin_button_x + origin_button_width and 
        origin_button_y <= mouse_y <= origin_button_y + origin_button_height):
        return True
    
    return False

def draw_wall_following_button(screen):
    """绘制Wall-following按钮"""
    # 绘制按钮背景
    pygame.draw.rect(screen, PURPLE, (wall_following_button_x, wall_following_button_y, wall_following_button_width, wall_following_button_height))
    
    # 绘制按钮边框
    pygame.draw.rect(screen, BLACK, (wall_following_button_x, wall_following_button_y, wall_following_button_width, wall_following_button_height), 2)
    
    # 绘制按钮文字
    try:
        font = pygame.font.SysFont('simhei', 14)
    except:
        font = pygame.font.Font(None, 14)
    
    button_text = font.render(f"{current_algorithm}", True, WHITE)
    text_rect = button_text.get_rect(center=(wall_following_button_x + wall_following_button_width//2 - 10, wall_following_button_y + wall_following_button_height//2))
    screen.blit(button_text, text_rect)
    
    # 绘制下拉箭头
    arrow_x = wall_following_button_x + wall_following_button_width - 15
    arrow_y = wall_following_button_y + wall_following_button_height//2
    if dropdown_open:
        # 向上箭头
        pygame.draw.polygon(screen, WHITE, [
            (arrow_x, arrow_y + 5),
            (arrow_x - 5, arrow_y - 5),
            (arrow_x + 5, arrow_y - 5)
        ])
    else:
        # 向下箭头
        pygame.draw.polygon(screen, WHITE, [
            (arrow_x, arrow_y - 5),
            (arrow_x - 5, arrow_y + 5),
            (arrow_x + 5, arrow_y + 5)
        ])
    
    # 绘制下拉菜单
    if dropdown_open:
        menu_y = wall_following_button_y + wall_following_button_height
        for i, algorithm in enumerate(algorithms):
            if algorithm != current_algorithm:
                menu_item_y = menu_y + i * 25
                pygame.draw.rect(screen, LIGHT_BLUE, (wall_following_button_x, menu_item_y, wall_following_button_width, 25))
                pygame.draw.rect(screen, BLACK, (wall_following_button_x, menu_item_y, wall_following_button_width, 25), 1)
                
                menu_text = font.render(algorithm, True, BLACK)
                menu_text_rect = menu_text.get_rect(center=(wall_following_button_x + wall_following_button_width//2, menu_item_y + 12))
                screen.blit(menu_text, menu_text_rect)

def handle_wall_following_button_click(mouse_pos):
    """处理Wall-following按钮点击"""
    global dropdown_open, current_algorithm
    
    mouse_x, mouse_y = mouse_pos
    
    # 检查是否点击了主按钮
    if (wall_following_button_x <= mouse_x <= wall_following_button_x + wall_following_button_width and 
        wall_following_button_y <= mouse_y <= wall_following_button_y + wall_following_button_height):
        dropdown_open = not dropdown_open
        return "toggle"
    
    # 检查是否点击了下拉菜单项
    if dropdown_open:
        menu_y = wall_following_button_y + wall_following_button_height
        for i, algorithm in enumerate(algorithms):
            if algorithm != current_algorithm:
                menu_item_y = menu_y + i * 25
                if (wall_following_button_x <= mouse_x <= wall_following_button_x + wall_following_button_width and 
                    menu_item_y <= mouse_y <= menu_item_y + 25):
                    current_algorithm = algorithm
                    dropdown_open = False
                    return "select"
    
    return None

def main():
    # 创建窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("DFS迷宫寻路 - 8x8")
    
    # 创建迷宫和机器人
    maze = Maze()
    robot = Robot(maze)
    
    # 速度控制
    robot_speed = 5  # 机器人移动速度（帧数间隔）
    speed_counter = 0
    
    # 游戏循环
    clock = pygame.time.Clock()
    running = True
    start_time = pygame.time.get_ticks()
    dfs_running = False
    dfs_paused = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 处理Reset按钮点击
                if handle_reset_button_click(event.pos):
                    robot.reset_dfs()
                    dfs_running = False
                    dfs_paused = False
                    speed_counter = 0
                    start_time = pygame.time.get_ticks()
                # 处理Shuffle按钮点击
                elif handle_shuffle_button_click(event.pos):
                    maze.generate_random_maze()
                    robot.reset_dfs()
                    dfs_running = False
                    dfs_paused = False
                    speed_counter = 0
                    start_time = pygame.time.get_ticks()
                # 处理Origin按钮点击
                elif handle_origin_button_click(event.pos):
                    maze.restore_original()
                    robot.reset_dfs()
                    dfs_running = False
                    dfs_paused = False
                    speed_counter = 0
                    start_time = pygame.time.get_ticks()
                # 处理Wall-following按钮点击
                elif handle_wall_following_button_click(event.pos):
                    # 下拉菜单处理在handle_wall_following_button_click中完成
                    pass
                # 处理滑动按钮点击
                new_speed = handle_slider_click(event.pos)
                if new_speed is not None:
                    robot_speed = new_speed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # 按R键重新生成迷宫
                    maze = Maze()
                    robot = Robot(maze)
                    start_time = pygame.time.get_ticks()
                    dfs_running = False
                    dfs_paused = False
                elif event.key == pygame.K_SPACE:  # 按空格键开始/暂停DFS
                    if not dfs_running and not robot.dfs_complete:
                        dfs_running = True
                        dfs_paused = False
                    elif dfs_running:
                        dfs_paused = not dfs_paused
                elif event.key == pygame.K_c:  # 按C键重置DFS
                    robot.reset_dfs()
                    dfs_running = False
                    dfs_paused = False
                    speed_counter = 0  # 重置速度计数器
                    start_time = pygame.time.get_ticks()  # 重置主计时器
                elif event.key == pygame.K_ESCAPE:  # 按ESC键退出
                    running = False
        
        # 执行搜索算法（使用速度控制）
        if dfs_running and not dfs_paused and not robot.dfs_complete:
            speed_counter += 1
            if speed_counter >= robot_speed:
                # 根据选择的算法执行不同的搜索
                if current_algorithm == "Wall-follow":
                    robot.wall_follow_search(robot_speed)
                elif current_algorithm == "Greedy":
                    robot.greedy_search()
                elif current_algorithm == "DFS":
                    robot.dfs_search()
                elif current_algorithm == "BFS":
                    robot.bfs_search()
                elif current_algorithm == "Flood-filled":
                    robot.flood_filled_search()
                elif current_algorithm == "A*":
                    robot.astar_search()
                speed_counter = 0
        
        # 更新转向动画
        robot.update_turning_animation()
        
        # 让机器人用传感器系统走到终点
        if robot.dfs_complete and robot.position != robot.maze.goal:
            speed_counter += 1
            if speed_counter >= robot_speed:
                robot.move_to_goal_with_sensors()
                speed_counter = 0
        
        # 更新计时器
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) // 1000
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        
        # 绘制
        screen.fill(WHITE)
        maze.draw(screen, robot)
        
        # 绘制速度调节滑动按钮
        draw_speed_slider(screen, robot_speed)
        
        # 绘制Reset按钮
        draw_reset_button(screen)
        
        # 绘制Shuffle按钮
        draw_shuffle_button(screen)
        
        # 绘制Origin按钮
        draw_origin_button(screen)
        
        # 绘制Wall-following按钮
        draw_wall_following_button(screen)
        
        # 显示计时器
        try:
            font = pygame.font.SysFont('simhei', 36)  # 使用黑体
        except:
            try:
                font = pygame.font.SysFont('microsoftyahei', 36)  # 使用微软雅黑
            except:
                font = pygame.font.Font(None, 36)  # 备用字体
        timer_text = font.render(f"{minutes}:{seconds}", True, BLACK)
        screen.blit(timer_text, (10, WINDOW_HEIGHT - 40))
        
        # 显示DFS状态信息
        try:
            font_small = pygame.font.SysFont('simhei', 20)  # 使用黑体
        except:
            try:
                font_small = pygame.font.SysFont('microsoftyahei', 20)  # 使用微软雅黑
            except:
                font_small = pygame.font.Font(None, 20)  # 备用字体
        
        # 算法计时器（根据选择的算法动态显示）
        if robot.is_running:
            if robot.dfs_complete and robot.end_time:
                dfs_time = (robot.end_time - robot.start_time) // 1000
                dfs_minutes = dfs_time // 60
                dfs_seconds = dfs_time % 60
                algorithm_timer_text = font_small.render(f"{current_algorithm}用时: {dfs_minutes}:{dfs_seconds:02d}", True, GREEN)
            else:
                dfs_time = (current_time - robot.start_time) // 1000
                dfs_minutes = dfs_time // 60
                dfs_seconds = dfs_time % 60
                algorithm_timer_text = font_small.render(f"{current_algorithm}用时: {dfs_minutes}:{dfs_seconds:02d}", True, RED)
            screen.blit(algorithm_timer_text, (10, WINDOW_HEIGHT - 60))
        
        
        # 显示DFS状态
        if robot.position == robot.maze.goal:
            status_text = font_small.render("🎯 已到达终点！", True, GREEN)
            screen.blit(status_text, (WINDOW_WIDTH - 200, 10))
        elif robot.dfs_complete and robot.position != robot.maze.goal:
            status_text = font_small.render("🚀 正在移动到终点...", True, BLUE)
            screen.blit(status_text, (WINDOW_WIDTH - 200, 10))
        elif robot.dfs_complete:
            status_text = font_small.render("✓ DFS完成！", True, GREEN)
            screen.blit(status_text, (WINDOW_WIDTH - 200, 10))
        elif dfs_running and not dfs_paused:
            status_text = font_small.render("DFS运行中...", True, RED)
            screen.blit(status_text, (WINDOW_WIDTH - 200, 10))
        elif dfs_paused:
            status_text = font_small.render("DFS已暂停", True, YELLOW)
            screen.blit(status_text, (WINDOW_WIDTH - 200, 10))
        else:
            status_text = font_small.render("按空格开始DFS", True, GRAY)
            screen.blit(status_text, (WINDOW_WIDTH - 200, 10))
        
        pygame.display.flip()
        clock.tick(10)  # 降低帧率以便观察DFS过程
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
