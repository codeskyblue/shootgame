# 1 - Import library
import math
import random
import pygame
from pygame.locals import *

class Resource(object):
    def __init__(self, image_file, screen, angle=0):
        self._origimage = pygame.image.load(image_file)
        self._image = pygame.transform.rotate(self._origimage, angle)
        self._screen = screen
        self.pos = [100, 100]
        self.step = 5

    def move(self, direction):
        w, a, s, d = direction
        if w:
            self.pos[1] -= self.step
            self._image = pygame.transform.rotate(self._origimage, 90)
        if a:
            self.pos[0] -= self.step
        if s:
            self.pos[1] += self.step
        if d:
            self.pos[0] += self.step

        x, y = self.pos
        width, height = self._image.get_width(), self._image.get_height()
        self.pos[0] = min(640-width, max(0, x))
        self.pos[1] = min(480-height, max(0, y))

    def draw(self):
        self.blit(self.pos)

    def blit(self, rect):
        self._screen.blit(self._image, rect)

class Player(Resource):
    def __init__(self, *args):
        super(Player, self).__init__(*args)
        # print direction



class ShootGame():
    def __init__(self):  
        # 2 - Initialize the game
        pygame.init()
        pygame.mixer.init()

        width, height = 640, 480
        self.screen=pygame.display.set_mode((width, height))
        self.acc=[0,0]
        self.arrows=[]

        self.initGraphics()
        self.initSound()


        self.badtimer=100
        self.badtimer1=0
        self.badguys=[[640,100]]
        self.healthvalue=194

        self.keys = [False, False, False, False]
        self.playerpos=[100,100]
        self.clock = pygame.time.Clock()

    def initGraphics(self):
        # 3 - Load images
        player = pygame.image.load("resources/images/dude.png")
        grass = pygame.image.load("resources/images/grass.png")
        castle = pygame.image.load("resources/images/castle.png")
        arrow = pygame.image.load("resources/images/bullet.png")
        badguyimg1 = pygame.image.load("resources/images/badguy.png")
        healthbar = pygame.image.load("resources/images/healthbar.png")
        health = pygame.image.load("resources/images/health.png")
        gameover = pygame.image.load("resources/images/gameover.png")
        youwin = pygame.image.load("resources/images/youwin.png")
        badguyimg=badguyimg1

        self.player = Player("resources/images/dude.png", self.screen)

    def initSound(self):
        # 3.1 - Load audio
        hit = pygame.mixer.Sound("resources/audio/explode.wav")
        enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
        shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        hit.set_volume(0.05)
        enemy.set_volume(0.05)
        shoot.set_volume(0.05)
        pygame.mixer.music.load('resources/audio/moonlight.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)

    def update(self):
        self.clock.tick(90)
        self.screen.fill(0)
        # 5 - clear the screen before drawing it again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.keys[0] = True
                elif event.key == K_a:
                    self.keys[1] = True
                elif event.key == K_s:
                    self.keys[2] = True
                elif event.key == K_d:
                    self.keys[3] = True
            if event.type == pygame.KEYUP:
                if event.key == K_w:
                    self.keys[0] = False
                elif event.key == K_a:
                    self.keys[1] = False
                elif event.key == K_s:
                    self.keys[2] = False
                elif event.key == K_d:
                    self.keys[3] = False
        self.player.move(self.keys)
        self.player.draw()

        pygame.display.flip()


    def finish(self):
        pass

game = ShootGame()
while True:
    game.update()
