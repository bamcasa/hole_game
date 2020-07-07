import pygame
import sys
import random
import numpy as np
import pprint

pygame.init()

class hole_game:
    def __init__(self):
        self.FPS = 30
        self.screen_size = (500,850)
        self.square_size = 3
        self.screen = pygame.display.set_mode(self.screen_size)
        self.square = np.zeros((self.square_size,self.square_size))
        pygame.display.set_caption("Hole game")
    def show_background(self):
        pygame.draw.rect(self.screen, (243, 216, 141),(0,0,self.screen_size[0],self.screen_size[1])) #모든 화면 노란색으로 채우기
    def show_square(self):
        pygame.draw.rect(self.screen, (222, 255, 222), [50, 50, 400, 400])
        pygame.draw.rect(self.screen, (255, 255, 255), [50, 50, 400, 400], 5)  #테두리
        for i in range(self.square_size):
            for j in range(self.square_size):
                if self.square[i][j]:
                    pygame.draw.circle(self.screen, (255,255,255), [i * 150 + 100, j * 150 + 100], 40)
                    pygame.draw.circle(self.screen, (190,190,190), [i * 150 + 100, j * 150 + 100], 40,2)

    def make_square(self):
        for i in range(self.square_size):
            for j in range(self.square_size):
                self.square[i][j] = random.randrange(0,2)
    def main(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.make_square()
            self.show_background()
            self.show_square()
            pygame.display.flip()

if __name__ == "__main__":
    hole_game().main()