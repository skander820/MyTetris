#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2019/6/20 11:12
# @Author  : Wu Yingfan
# @Email   : yingfan.w@sunyard.com
# @File    : main.py
# from lib.mainWin import MainWin
import pygame
from pygame import *
import sys, numpy as np
import config, random
from squares import shapes
from pygame.locals import *

pygame.init()
FONT_BASE = pygame.font.Font('freesansbold.ttf', 18)  # 字体
FONT_BIG = pygame.font.Font('freesansbold.ttf', 100)


def draw_text(text, font, color):
    surf = font.render(text, True, color)
    return surf, surf.get_rect()


def check_key_press():
    for evt in pygame.event.get([KEYDOWN, KEYUP, QUIT]):
        if evt.type == KEYDOWN:
            continue
        if evt.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        return evt.key
    return None


class MainWin:

    def __init__(self):
        pygame.init()
        self.screen = None
        self.score = 0
        self.level = 0
        self.clock = None
        self.current = None
        self.time = pygame.time.get_ticks()
        self.move_time = pygame.time.get_ticks()
        self.cycle = config.cycle
        self.board = np.zeros((config.num_x, config.num_y), dtype=np.int)
        self.next = self.get_new_square()
        self.spare = None
        self.left_status = False
        self.right_status = False
        self.down_status = False

    @staticmethod
    def get_font(size):
        return pygame.font.Font('freesansbold.ttf', size)

    def run(self):
        self.screen = pygame.display.set_mode([config.main_weight, config.main_height])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('MyTetris')
        self.screen.fill(config.color_bg)
        while True:
            self.clock.tick(30)
            if self.game_process():
                break

    def game_process(self):
        self.screen.fill(config.color_bg)
        pygame.draw.rect(self.screen, config.color_main_board_line, config.main_board_rect, config.size_main_board_line)
        pygame.display.update()
        self.draw_spare()
        while True:
            self.clock.tick(30)
            now = pygame.time.get_ticks()
            move_now = pygame.time.get_ticks()
            if move_now - self.move_time >= config.min_move_gap:
                self.move_status()
                self.move_time=move_now
            if not self.current:
                self.check()
                self.show_score()
                if np.sum(self.board[:, 0]) > 0:
                    break
                self.current = self.next
                self.next = self.get_new_square()
                self.draw_next()
            if now - self.time >= self.cycle:  # 如果时间间隔超过当前的cycle
                self.move(0, 1)  # 方块下落生成等过程
                self.time = now
            self.draw(config.main_board_rect, self.board)
            pygame.display.update(config.main_board_rect)  # 刷新
            for evt in pygame.event.get():  # 退出
                if evt.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evt.type == pygame.KEYDOWN:
                    if evt.key == K_LEFT:
                        self.left_status = True
                    elif evt.key == K_RIGHT:
                        self.right_status = True
                    elif evt.key == K_UP:
                        self.trans()
                    elif evt.key == K_DOWN:
                        self.down_status = True
                    elif evt.key == K_SPACE:
                        self.swap()
                elif evt.type == pygame.KEYUP:
                    if evt.key == K_LEFT:
                        self.left_status = False
                    elif evt.key == K_RIGHT:
                        self.right_status = False
                    elif evt.key == K_DOWN:
                        self.down_status = False
        self.board.fill(0)
        surface, rect = draw_text('GameOver', self.get_font(30), (0, 0, 0))
        rect.center = pygame.Rect(config.main_board_rect).center
        self.screen.blit(surface, rect)
        while check_key_press() is None:
            pygame.display.update()

    def move_status(self):
        if self.left_status:
            self.move(-1, 0)
        if self.right_status:
            self.move(1, 0)
        if self.down_status:
            self.move(0, 1)

    def swap(self):
        self.draw_current(False)
        if not self.is_swap_collide():
            self.current, self.spare = self.spare, self.current
            if not self.current:
                self.current = self.next
                self.next = self.get_new_square()
            else:
                self.current['x'] = self.spare['x']
                self.current['y'] = self.spare['y']
            self.draw_next()
            self.draw_spare()
        self.draw_current(True)

    def trans(self):
        self.draw_current(False)
        if not self.is_collide(rotation=1):
            self.current['rotation'] += 1
        self.draw_current(True)

    def move(self, x, y):
        if self.current:
            self.draw_current(False)
            if self.is_collide(x=x, y=y):
                self.draw_current(True)
                if y != 0:
                    self.current = None
            else:
                self.current['x'] += x
                self.current['y'] += y
                self.draw_current(True)

    def is_collide(self, x=0, y=0, rotation=0) -> bool:
        for xi, yi in self.get_current_coordinate(rotation):  # 拿到current的不为空白坐标
            x_board = self.current['x'] + x + xi  # 找出移动后 不为空白的点在board中的坐标
            y_board = self.current['y'] + y + yi
            if (x_board in range(config.num_x)) and y_board < config.num_y:  # 如果移动后  有点在board外面 就是碰撞了
                if self.board[x_board, y_board] == 1:  # 如果要移动的点已经不为空白  碰撞了
                    return True
            else:
                return True
        return False

    def is_swap_collide(self):
        if self.spare:
            for xi, yi in self.get_square_coordinate(self.spare):
                x_board = self.current['x'] + xi
                y_board = self.current['y'] + yi
                if (x_board in range(config.num_x)) and y_board < config.num_y:
                    if self.board[x_board, y_board] == 1:
                        return True
                else:
                    return True
        return False

    def get_current(self, rotation) -> np.ndarray:
        return self.get_square_array(self.current, rotation)

    @staticmethod
    def get_square_array(square, rotation):
        return np.asarray(shapes[square['shape']])[(square['rotation'] + rotation) % square['len'], :,
               :]

    def get_current_coordinate(self, rotation=0):
        return zip(*np.where(self.get_current(rotation) == 1))

    def get_square_coordinate(self, square, rotation=0):
        return zip(*np.where(self.get_square_array(square, rotation) == 1))

    def draw_current(self, flag=True):
        for xi, yi in self.get_current_coordinate():
            x = self.current['x'] + xi
            y = self.current['y'] + yi
            if (x in range(config.num_x)) & (y in range(config.num_y)):
                if flag:
                    if self.board[x, y] == 0:
                        self.board[x, y] = 1
                else:
                    if self.board[x, y] == 1:
                        self.board[x, y] = 0

    def draw_next(self):
        surface, rect = draw_text(f'next', self.get_font(24), (0, 0, 0))
        rect.center = pygame.Rect(config.next_board_rect.move(-60, -90)).center
        self.screen.blit(surface, rect)
        pygame.display.update(rect)
        self.draw(config.next_board_rect.move(0, 30), self.get_square_array(self.next, 0))
        pygame.display.update(config.next_board_rect.move(0, 30))

    def draw_spare(self):
        surface, rect = draw_text(f'swap', self.get_font(24), (0, 0, 0))
        rect.center = pygame.Rect(config.next_board_rect.move(60, -90)).center
        self.screen.blit(surface, rect)
        pygame.display.update(rect)
        if self.spare:
            self.draw(config.next_board_rect.move(120, 30), self.get_square_array(self.spare, 0))
            pygame.display.update(config.next_board_rect.move(120, 0))

    def check(self):
        (lines,) = np.where(np.sum(self.board, axis=0) == config.num_x)
        lines = list(lines)
        if len(lines) > 0:
            lines.sort()
            for line in lines:
                self.board[:, 1:line + 1] = self.board[:, 0:line]
                self.board[:, 0] = 0
            self.score += 100 * (2 ** (len(lines) - 1))
            self.level = self.score // 2000 if self.score // 2000 <= 10 else 10
            self.cycle = config.cycle // config.level[self.level]

    def show_score(self):
        surface, rect = draw_text(f'score: {self.score}', self.get_font(30), (0, 0, 0))
        rect.center = pygame.Rect(config.score_board_rect).center
        self.screen.blit(surface, rect)
        pygame.display.update(rect)

    @staticmethod
    def get_new_square():
        square = {
            'shape': random.choice(list(shapes.keys())),
            'x': random.randint(0, 5),
            'y': -2,
        }
        square.setdefault('len', len(shapes[square['shape']]))
        square.setdefault('rotation', random.randint(0, square['len']))
        return square

    def draw(self, board, ndboard):
        for x, y in [self.get_abs(*p, board=board) for p in zip(*np.where(ndboard == 0))]:
            pygame.draw.rect(self.screen, (255, 255, 255),
                             (x, y, config.base_square_weight, config.base_square_height), 1)
        for x, y in [self.get_abs(*p, board=board) for p in zip(*np.where(ndboard == 1))]:
            pygame.draw.rect(self.screen, config.color_main_board_line,
                             (x, y, config.base_square_weight, config.base_square_height), 1)

    def get_abs(self, x, y, board):
        return board.x + x * (config.base_square_weight + config.gap_square) + config.gap_square, \
               board.y + y * (config.base_square_height + config.gap_square) + config.gap_square


if __name__ == '__main__':
    MainWin().run()
