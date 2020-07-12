import pygame
import sys
import random
import numpy as np
import copy
import time
import pprint

pygame.init()

class hole_game:
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
        self.location = np.zeros((self.square_size,self.square_size),dtype = object)
        self.input = np.zeros((self.square_size,self.square_size))
        self.font = pygame.font.SysFont("notosanscjkkr", 30)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.square = np.zeros((self.square_count, self.square_size, self.square_size))
        self.correct_square = np.zeros((self.square_size, self.square_size))
        pygame.display.set_caption("Hole game")

    def show_background(self):
        pygame.draw.rect(self.screen, (243, 216, 141),(0, 0, self.screen_size[0], self.screen_size[1])) #모든 화면 노란색으로 채우기

    def show_square(self):
        pygame.draw.rect(self.screen, (233,233,233), [50, 50, 400, 400])
        pygame.draw.rect(self.screen, (190,190,190), [50, 50, 400, 400], 5)  #테두리
        if self.start:
            self.screen.blit(self.font.render(f"number {self.square_number + 1}", True, (50, 255, 255)), (215, 20))
            for i in range(self.square_size):
                for j in range(self.square_size):
                    if self.square[self.square_number][j][i]:
                        pygame.draw.circle(self.screen, (0,0,0), [i * 150 + 100, j * 150 + 100], 40)
                        #pygame.draw.circle(self.screen, (190, 190, 190), [i * 150 + 100, j * 150 + 100], 40, 2)

    def make_correct_hole(self, hole_count):
        self.correct_hole = []
        count = 0
        while (True):
            hole_x = random.randrange(0, self.square_size)
            hole_y = random.randrange(0, self.square_size)
            if [hole_y, hole_x] not in self.correct_hole:
                self.correct_hole.append([hole_y, hole_x])
                count += 1
            if count == hole_count:
                break
        print("correct_hole : ",self.correct_hole)


    def make_square(self,hole_count): #원하는 구멍의 개수 입력
        self.square = np.zeros((self.square_count, self.square_size, self.square_size)) #종이 초기화
        self.make_correct_hole(2)
        for k in range(self.square_count):
            self.hole = copy.deepcopy(self.correct_hole)
            count = 0
            while (True):
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
        check = 0 # 정답 유무 체크용 -> 변수명 바꿔야 할 듯...
        for i in range(self.square_size):
            for j in range(self.square_size):
                for k in range(self.square_count):
                    sum += self.square[k][i][j]
                if(sum == self.square_count):
                    self.correct_square[i][j] = 1
                    check += 1 # 정답있을 때 1 증가
                sum = 0

        if check == 0:
            print("정답 없으므로 재추첨")
            self.make_square(2) # 3번마다 사각형 값 초기화,1~9까지의 랜덤값 입력

        #pprint.pprint(self.correct_square)

    def show_answer_square(self):
        pygame.draw.rect(self.screen, (233,233,233), [100, 500, 300, 300])
        pygame.draw.rect(self.screen, (190,190,190), [100, 500, 300, 300], 5)  # 테두리
        for i in range(self.square_size):
            for j in range(self.square_size):
                if self.input[j][i]:
                    pygame.draw.circle(self.screen, (0,0,0), [i * 100 + 150, j * 100 + 550], 30)
                self.location[i][j] = pygame.draw.circle(self.screen, (0,0,0), [i * 100 + 150, j * 100 + 550],
                                                         30, 2)

    def click(self,pos):
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
            self.inputbutton = pygame.draw.rect(self.screen, (190, 190, 190), [0, 800, 500, 100])
            self.screen.blit(self.font.render("Input", True, (0, 0, 0)), (220, 845))
    def gamestart(self):
        self.start = True
        time.sleep(1)
        self.square_number += 1
        if (self.square_number >= self.square_count):
            self.button = True
            self.start = False
    def examine_input(self):
        print("----------------------")
        print(self.input,type(self.input))
        print(self.correct_square,type(self.correct_square))
        if (self.input==self.correct_square).all(): #입력값과 정답이 같은지 비교
            self.answer = 1
        else:
            self.answer = 2
    def show_answer(self):
        if self.answer == 1:
            print("O")
            pygame.draw.rect(self.screen, (0,0,0), [50, 300, 400, 200])
            pygame.draw.rect(self.screen, (233, 233, 233), [50, 300, 400, 200], 5)
            self.screen.blit(self.font.render("YES", True, (255,255,255)), (200,400))
        elif self.answer == 2:
            print("X")
            pygame.draw.rect(self.screen, (0,0,0), [50, 300, 400, 200])
            pygame.draw.rect(self.screen, (233, 233, 233), [50, 300, 400, 200], 5)
            self.screen.blit(self.font.render("NO", True, (255,255,255)), (200,400))

    def main(self):
        clock = pygame.time.Clock()
        self.make_square(2) # 3번마다 사각형 값 초기화,1~9까지의 랜덤값 입력
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
    hole_game().main()