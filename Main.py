import pygame
import sys
import random

pygame.init()

class hole_game:
    def __init__(self):
        self.FPS = 30
        self.screen = pygame.display.set_mode((500,800))
        pygame.display.set_caption("Hole game")
    def show(self):
        pygame.draw.rect(self.screen, (243, 216, 141),(0,0, 500,800))
        pygame.draw.rect(self.screen, (190, 190, 190), [100, 200, 400, 200])
        pygame.draw.rect(self.screen, (255, 255, 255), [100, 200, 400, 200], 5)
    def main(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.show()
            pygame.display.flip()

if __name__ == "__main__":
    hole_game().main()