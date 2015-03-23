# 1 - Import library
import math
import time
# import random
import pygame
from pygame.locals import *
from PodSixNet.Connection import ConnectionListener, connection
from sys import stdin

class ShootGame(ConnectionListener):
    def __init__(self):
        # 2 - Initialize the game
        self.Connect(("localhost", 12321))
        connection.Send({"action": "nickname", "nickname": "pig"})
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
        self.playerangle = 0
        self.playerdest = self.playerpos
        self.playerspeed = 2
        self.playershootcd = pygame.time.get_ticks()
        self.clock = pygame.time.Clock()
        self.lagduration = 0.1

        # update ping time
        pygame.time.set_timer(pygame.USEREVENT, 1000)

    def Network(self, data):
        print 'receive:', data

    def Network_error(self, data):
        print 'network error', data['error'][1]
        connection.Close()

    def Network_disconnected(self, data):
        print 'Server disconnected'
        exit()
        
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
        #pygame.mixer.music.play(-1, 0.0)
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

    def Network_selfpos(self, data):
        x = data['x']
        y = data['y']
        print data
        self.playerdest = [x, y]

    def Network_pong(self, data):
        print time.time()
        self.lagduration = time.time() - float(data['timestamp'])
        print 'lag', self.lagduration

    def drawPlayer(self):
        # if self.keys[0]:
        #     self.playerpos[1] -= 5
        # if self.keys[1]:
        #     self.playerpos[0] -= 5
        # if self.keys[2]:
        #     self.playerpos[1] += 5
        # if self.keys[3]:
        #     self.playerpos[0] += 5o
        # Move player to destination
        if abs(self.playerpos[0] - self.playerdest[0]) > 5 or \
            abs(self.playerpos[1] - self.playerdest[1]) > 5:
            cx, cy = self.playerpos
            dx, dy = self.playerdest
            radius = math.atan2(dy-cy, dx-cx)
            self.playerangle = 360-radius/math.pi*180
            #self.player = pygame.transform.rotate(self.player, 360-angle/math.pi*180)
            nx = cx + math.cos(radius)*self.playerspeed
            ny = cy + math.sin(radius)*self.playerspeed
            self.playerpos = [nx, ny]

        # if angle:
        player = pygame.transform.rotate(self.player, self.playerangle)
        rect = player.get_rect()
        rect.centerx = self.playerpos[0]
        rect.centery = self.playerpos[1]
        self.screen.blit(player, rect)#self.playerpos)

    def drawBadguy(self):
        for badguy in self.badguys:
            self.screen.blit(self.badguyimg, badguy)

    def drawOther(self):
        font = pygame.font.Font(None, 20)
        if self.lagduration:
            msec = int(self.lagduration*1000)
            ping = font.render('Ping: '+str(msec), True, (255, 255, 0))
            pos = (self.screen.get_width() - ping.get_width()*1.5, 50)
            self.screen.blit(ping, pos)
        fpslabel = font.render('FPS: '+str(int(self.clock.get_fps())), True, (255, 255, 0))
        pos = (self.screen.get_width() - ping.get_width()*1.5, 20)
        self.screen.blit(fpslabel, pos)

    def update(self):
        connection.Pump()
        self.Pump()

        self.clock.tick(90)
        self.screen.fill(0)

        self.drawGrass()
        self.drawArrows()
        self.drawPlayer()
        self.drawBadguy()
        self.drawOther()

        # 5 - clear the screen before drawing it again
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            
            if event.type == pygame.USEREVENT:
                connection.Send({'action': 'ping', 'timestamp': str(time.time())})
            elif event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    self.keys[0] = True
                elif event.key == K_a:
                    self.keys[1] = True
                elif event.key == K_s:
                    self.playerdest = self.playerpos[:]
                elif event.key == K_d:
                    self.keys[3] = True
            elif event.type == pygame.KEYUP:
                if event.key == K_w:
                    self.keys[0] = False
                elif event.key == K_a:
                    self.keys[1] = False
                elif event.key == K_s:
                    self.keys[2] = False
                elif event.key == K_d:
                    self.keys[3] = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # right click
                #if event.button == 3: 
                self.playerdest = pygame.mouse.get_pos()
                connection.Send({'action': 'playerdest', 'dest': self.playerdest})
                # left click
                if event.button == 2:
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

