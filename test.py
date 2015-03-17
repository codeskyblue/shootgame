# 1 - Import library
import math
# import random
import pygame
from pygame.locals import *

class ShootGame():
    def __init__(self):  
        # 2 - Initialize the game
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()

        self.width = 640
        self.height = 480
        self.screen=pygame.display.set_mode((self.width, self.height))
        self.acc=[0,0]
        self.arrows=[]

        self.initGraphics()
        self.initSound()


        self.badtimer=100
        self.badtimer1=0
        self.badguys=[[300,100]]
        self.healthvalue=194

        self.keys = [False, False, False, False]
        self.playerpos=[100,100]
        self.playershootcd = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()

    def initGraphics(self):
        # 3 - Load images
        healthbar = pygame.image.load("resources/images/healthbar.png")
        health = pygame.image.load("resources/images/health.png")
        gameover = pygame.image.load("resources/images/gameover.png")
        youwin = pygame.image.load("resources/images/youwin.png")
        # badguyimg=badguyimg1

        self.badguyimg = pygame.image.load("resources/images/badguy.png")
        self.player = pygame.image.load("resources/images/dude.png")
        self.arrow = pygame.image.load("resources/images/bullet.png")
        self.grass = pygame.image.load("resources/images/grass.png")
        # self.castle = pygame.image.load("resources/images/castle.png")

    def initSound(self):
        # 3.1 - Load audio
        hit = pygame.mixer.Sound("resources/audio/explode.wav")
        enemy = pygame.mixer.Sound("resources/audio/enemy.wav")
        self.shoot = pygame.mixer.Sound("resources/audio/shoot.wav")
        hit.set_volume(0.05)
        enemy.set_volume(0.05)
        self.shoot.set_volume(0.05)
        pygame.mixer.music.load('resources/audio/moonlight.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)

    def drawGrass(self):
        w, h = self.screen.get_width(), self.screen.get_height()
        for x in range(w/self.grass.get_width()+1):
            for y in range(h/self.grass.get_height()+1):
                self.screen.blit(self.grass, (x*self.grass.get_width(), y*self.grass.get_height()))

    def drawArrows(self):
        for idx, bullet in enumerate(self.arrows):
            arrow = pygame.transform.rotate(self.arrow, 360-bullet[0]/math.pi*180)
            bullet[1] += math.cos(bullet[0])*10
            bullet[2] += math.sin(bullet[0])*10
            self.screen.blit(arrow, bullet[1:])
            if bullet[1] > self.width or bullet[1] < 0 or \
                bullet[2] > self.height or bullet[2] < 0:
                self.arrows.pop(idx)

    def drawPlayer(self):
        if self.keys[0]:
            self.playerpos[1] -= 5
        if self.keys[1]:
            self.playerpos[0] -= 5
        if self.keys[2]:
            self.playerpos[1] += 5
        if self.keys[3]:
            self.playerpos[0] += 5
        self.screen.blit(self.player, self.playerpos)

    def drawBadguy(self):
        for badguy in self.badguys:
            self.screen.blit(self.badguyimg, badguy)

    def update(self):
        self.clock.tick(90)
        self.screen.fill(0)

        self.drawGrass()
        self.drawArrows()
        self.drawPlayer()
        self.drawBadguy()

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

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.time.get_ticks() > self.playershootcd:
                    self.playershootcd = pygame.time.get_ticks() + 600
                    self.shoot.play()
                    mx, my = pygame.mouse.get_pos()
                    x, y = self.playerpos
                    angle = math.atan2(my-y, mx-x)
                    self.arrows.append([
                        angle, x, y])

        pygame.display.flip()

    def finish(self):
        pass

game = ShootGame()
while True:
    game.update()

