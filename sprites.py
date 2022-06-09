import pygame as pg
from settings import *
import random

class Player(pg.sprite.Sprite):
    def __init__(self, x_loc, y_loc):
        # initialize sprite class
        pg.sprite.Sprite.__init__(self)

        # create the player rectangle
        self.image = pg.image.load('images/car-truck1.png')

        # get/set the rectangles coords

        self.rect = self.image.get_rect()
        self.rect.x = x_loc
        self.rect.y = y_loc

        # set the player speed
        self.x_velo = 0
        self.y_velo = 0

    def update(self):
        self.rect.x += self.x_velo
        self.rect.y += self.y_velo
        # if self.rect.x >= WIDTH-P_SIZE:
        #     self.rect.x = WIDTH-P_SIZE
        # elif self.rect.x <= 0:
        #     self.rect.x = 0
        if self.rect.right >= WIDTH-P_SIZE:
            self.rect.right = WIDTH-P_SIZE
        if self.rect.left <= 2*P_SIZE:
            self.rect.left = 2*P_SIZE
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.y <= 45:
            self.rect.y = HEIGHT - P_SIZE


class Enemy(pg.sprite.Sprite):
    def __init__(self, x_loc, y_loc, img):

        pg.sprite.Sprite.__init__(self)
        self.image = img

        self.rect = self.image.get_rect()

        self.rect.x = x_loc
        self.rect.y = y_loc

        self.y_velo = random.randint(2,5)


    def update(self):
        self.rect.y += self.y_velo

        if self.rect.top >= HEIGHT:
            self.kill()