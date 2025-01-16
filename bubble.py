import random
import pygame
import os

class Bubble:
    def __init__(self, RESOURCE_PATH, screen_width, screen_height):
        self.Siz = random.randint(10, 100)
        self.Pic = pygame.image.load(os.path.join(RESOURCE_PATH, "resource", "Buble.png"))
        self.x = random.randint(0, screen_width)
        self.y = screen_height - 50
        self.speed = random.randint(3, 10)
        self.angle = random.uniform(-1.1, 1.1)
        self.direction_change_prob = 0.4 
        self.frame_count = 0  # フレームカウント

    def move(self):
        self.y -= self.speed
        self.x += int(self.angle * 2)
        if random.random() < self.direction_change_prob:
            self.angle *= -1

        self.frame_count += 1
        if self.frame_count % 5 == 0:
            self.Siz -= 1

    def draw(self):
        Pic = pygame.transform.scale(self.Pic, (self.Siz, self.Siz))
        Screen.blit(Pic, (self.x, self.y))
    
    def checkDel(self):
        if self.Siz < 0 or self.y < -20:
            return True
        else:
            return False