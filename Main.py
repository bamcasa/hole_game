import pygame
import sys
import random
import numpy as np
import copy
import time
import pprint

pygame.init()

# 색 상수
ARMADILLO = (71, 66, 60)  # 배경색
PAMPAS = (240, 235, 229)  # 사각형 배경색, 페이지 텍스트 색
SILVER = (190, 190, 190)  # 사각형 테두리 색
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class HoleGame:
    def __init__(self):
        self.FPS = 30
        self.screen_size = (500, 900)
        self.square_size = 3
        self.square_count = 3
        self.square_number = -1
        self.answer = 0
        self.hole = []
        self.correct_hole = []
        self.start = False
        self.button = True
        self.pos = (0, 0)
        self.location = np.zeros((self.square_size, self.square_size), dtype=object)
        self.input = np.zeros((self.square_size, self.square_size))
        self.inputbutton = None  # inputbutton의 초기값을 뭘로 해야할지 모르겠슴다..
        self.font = pygame.font.SysFont("notosanscjkkr", 30)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.square = np.zeros((self.square_count, self.square_size, self.square_size))
        self.correct_square = np.zeros((self.square_size, self.square_size))
        pygame.display.set_caption("Hole game")

    def show_background(self):
        pygame.draw.rect(self.screen, ARMADILLO, (0, 0, self.screen_size[0], self.screen_size[1]))  # 배경 채우기

    def show_square(self):
        rect_position = [50, 40, 400, 400]

        pygame.draw.rect(self.screen, PAMPAS, rect_position)
        pygame.draw.rect(self.screen, SILVER, rect_position, 5)  # 테두리
        if self.start:
            self.screen.blit(self.font.render(f"Page {self.square_number + 1}", True, PAMPAS), (220, 10))
            for i in range(self.square_size):
                for j in range(self.square_size):
                    if self.square[self.square_number][j][i]:
                        pygame.draw.circle(self.screen, BLACK, [i * 150 + 100, j * 150 + 90], 40)

    def make_correct_hole(self, hole_count):
        self.correct_hole = []
        count = 0
        while True:
            hole_x = random.randrange(0, self.square_size)
            hole_y = random.randrange(0, self.square_size)
            if [hole_y, hole_x] not in self.correct_hole:
                self.correct_hole.append([hole_y, hole_x])
                count += 1
            if count == hole_count:
                break
        print("correct_hole : ", self.correct_hole)

    def make_square(self, hole_count):  # 원하는 구멍의 개수 입력
        self.square = np.zeros((self.square_count, self.square_size, self.square_size))  # 종이 초기화
        self.make_correct_hole(2)
        for k in range(self.square_count):
            self.hole = copy.deepcopy(self.correct_hole)
            count = 0
            while True:
                hole_x = random.randrange(0, self.square_size)  # 뚫린 구멍의 x좌표 생성
                hole_y = random.randrange(0, self.square_size)  # 뚫린 구멍의 y좌표 생성
                if [hole_y, hole_x] not in self.hole:
                    self.hole.append([hole_y, hole_x])  # 뚫린 구멍의 좌표를 리스트에 넣음
                    count += 1
                if count == hole_count:
                    break
            print(self.hole)

            for i in range(hole_count + len(self.correct_hole)):
                self.square[k][self.hole[i][0]][self.hole[i][1]] = 1
        self.make_answer_square()

    def make_answer_square(self):
        # 답 사각형 초기화
        self.correct_square = np.zeros((self.square_size, self.square_size))

        sum = 0
        for i in range(self.square_size):
            for j in range(self.square_size):
                for k in range(self.square_count):
                    sum += self.square[k][i][j]
                if sum == self.square_count:
                    self.correct_square[i][j] = 1
                sum = 0

    def show_answer_square(self):
        rect_position = [100, 472, 300, 300]

        pygame.draw.rect(self.screen, PAMPAS, rect_position)
        pygame.draw.rect(self.screen, SILVER, rect_position, 5)  # 테두리
        for i in range(self.square_size):
            for j in range(self.square_size):
                circle_position = [i * 100 + 150, j * 100 + 522]

                if self.input[j][i]:
                    pygame.draw.circle(self.screen, ARMADILLO, circle_position, 30)
                self.location[i][j] = pygame.draw.circle( self.screen, BLACK, circle_position, 30, 2)

    def click(self, pos):
        if self.inputbutton.collidepoint(pos):
            self.examine_input()
        for i in range(self.square_size):
            for j in range(self.square_size):
                if self.location[i][j].collidepoint(pos):
                    if self.input[j][i] == 1:
                        self.input[j][i] = 0
                    else:
                        self.input[j][i] = 1

    def show_inputbutton(self):
        if self.button:
            self.inputbutton = pygame.draw.rect(self.screen, SILVER, [0, 800, 500, 100])
            self.screen.blit(pygame.font.SysFont("notosanscjkkr", 50).render("Input", True, BLACK), (205, 835))

    def gamestart(self):
        self.start = True
        time.sleep(1)
        self.square_number += 1
        if self.square_number >= self.square_count:
            self.button = True
            self.start = False

    def examine_input(self):
        if (self.input == self.correct_square).all():  # 입력값과 정답값 비교
            self.answer = 1
        else:
            self.answer = 2

    def show_answer(self):
        rect_position = [50, 300, 400, 200]
        font_position = (230, 400)

        if self.answer == 1:
            pygame.draw.rect(self.screen, BLACK, rect_position)
            pygame.draw.rect(self.screen, WHITE, rect_position, 5)  # 테두리
            self.screen.blit(self.font.render("YES", True, WHITE), font_position)
        elif self.answer == 2:
            pygame.draw.rect(self.screen, BLACK, rect_position)
            pygame.draw.rect(self.screen, WHITE, rect_position, 5)  # 테두리
            self.screen.blit(self.font.render("NO", True, WHITE), font_position)

    def main(self):
        clock = pygame.time.Clock()
        self.make_square(2)  # 3번마다 사각형 값 초기화, 1 ~ 9까지의 랜덤값 입력
        while True:
            clock.tick(self.FPS)
            if self.start:
                self.gamestart()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.gamestart()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.pos = pygame.mouse.get_pos()
                    self.click(self.pos)
            self.show_background()
            self.show_square()
            self.show_answer_square()
            self.show_inputbutton()
            self.show_answer()

            pygame.display.flip()


if __name__ == "__main__":
    HoleGame().main()
