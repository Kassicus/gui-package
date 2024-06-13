import pygame
from settings import *
import spit

pygame.init()

class Window():
    def __init__(self):
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption("SPIT v0.0.1")

        self.running = True
        self.clock = pygame.time.Clock()
        self.events = pygame.event.get()

        self.text_box = spit.TextField(100, 100, 100, 30, "test", WHITE, GREEN, RED, draw_type="line")
        self.another_box = spit.TextField(100, 300, 250, 18, "another", WHITE, GREEN, RED, alignment="centered")

    def start(self):
        while self.running:
            self.event_loop()
            self.draw()
            self.update()

    def event_loop(self):
        self.events = pygame.event.get()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.running = False

    def draw(self):
        self.screen.fill(BLACK)

        self.text_box.draw()
        self.another_box.draw()

    def update(self):
        self.text_box.update(self.events)
        self.another_box.update(self.events)

        pygame.display.update()
        deltatime = self.clock.tick(framerate) / 1000

if __name__ == '__main__':
    w = Window()
    w.start()
    pygame.quit()