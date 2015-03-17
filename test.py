# 1 - Import library
import math
# import random
import pygame
from pygame.locals import *

class Resource(object):
    def __init__(self, image, screen, angle=0):
        if isinstance(image, basestring):
            self._origimage = pygame.image.load(image)
        else:
            self._origimage = image
        self._image = pygame.transform.rotate(self._origimage, -angle)
        self._screen = screen
        self._angle = angle
        self.pos = [100, 100]
        self.step = 5

    def move_angle(self, length=None, angle=None):
        if angle:
            self._angle = -angle
        if not length:
            length = self.step
        self._image = pygame.transform.rotate(self._origimage, self._angle)
        xoff = length * math.cos(self._angle/180.0*math.pi)
        yoff = length * math.sin(self._angle/180.0*math.pi)
        self.pos = [self.pos[0]+xoff, self.pos[1]+yoff]
        # fix pos
        x, y = self.pos
        width, height = self._image.get_width(), self._image.get_height()
        self.pos[0] = min(640-width, max(0, x))
        self.pos[1] = min(480-height, max(0, y))

    def move(self, direction):
        w, a, s, d = direction
        vec = [0, 0]
        if w:
            vec[1] -= 1
        if a:
            vec[0] -= 1
        if s:
            vec[1] += 1
        if d:
            vec[0] += 1
        if vec[0] != 0 or vec[1] != 0:
            angle = math.atan2(vec[1], vec[0])*180.0/math.pi
            self.move_angle(self.step, angle)

    def draw(self):
        self.blit(self.pos)

    def blit(self, rect):
        self._screen.blit(self._image, rect)

class Player(Resource):
    def __init__(self, *args):
        super(Player, self).__init__(*args)

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
        self.badguys=[[640,100]]
        self.healthvalue=194

        self.keys = [False, False, False, False]
        self.playerpos=[100,100]
        self.clock = pygame.time.Clock()

    def initGraphics(self):
        # 3 - Load images
        player = pygame.image.load("resources/images/dude.png")
        castle = pygame.image.load("resources/images/castle.png")
        badguyimg1 = pygame.image.load("resources/images/badguy.png")
        healthbar = pygame.image.load("resources/images/healthbar.png")
        health = pygame.image.load("resources/images/health.png")
        gameover = pygame.image.load("resources/images/gameover.png")
        youwin = pygame.image.load("resources/images/youwin.png")
        badguyimg=badguyimg1

        self.player = pygame.image.load("resources/images/dude.png")
        self.arrow = pygame.image.load("resources/images/bullet.png")
        self.grass = pygame.image.load("resources/images/grass.png")

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

    def update(self):
        self.clock.tick(90)
        self.screen.fill(0)

        self.drawGrass()
        self.drawArrows()
        self.drawPlayer()

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
                self.shoot.play()
                mx, my = pygame.mouse.get_pos()
                x, y = self.playerpos
                angle = math.atan2(my-y, mx-x)
                self.arrows.append([
                    angle, x, y])

        # self.player.move(self.keys)
        # self.player.draw()

        pygame.display.flip()

    def finish(self):
        pass

game = ShootGame()
while True:
    game.update()

