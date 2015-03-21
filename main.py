#!/usr/bin/env python
# coding: utf-8
#

#1 - Import library
import math
import random
import pygame
from pygame.locals import *
from sys import exit
#2 - Initialize the game
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

keys = [False]*4
arrawkeys = [K_w, K_a, K_s, K_d]
playerpos = [100, 100]
acc = [0, 0]
arrows = []

badtimer = 100
badtimer1 = 0
badguys = [[640, 100]]
healthvalue = 194
#3 - Load images
player = pygame.image.load("resources/images/dude.png")
grass = pygame.image.load("resources/images/grass.png")
castle = pygame.image.load("resources/images/castle.png")
arrow = pygame.image.load("resources/images/bullet.png")
badguyimg1 = pygame.image.load("resources/images/badguy.png")
badguyimg = badguyimg1
healthbar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
def blit_center(obj, pos):
    lefttop = pos[0]-obj.get_width()/2, pos[1]-obj.get_height()/2
    screen.blit(obj, lefttop)

while True:
    badtimer -= 1
    #5 - Clear the screen before drawing again
    screen.fill(0)
    for x in range(width/grass.get_width()+1):
        for y in range(height/grass.get_height()+1):
            screen.blit(grass, (x*100, y*100))
    screen.blit(castle, (0, 30))
    screen.blit(castle, (0, 135))
    screen.blit(castle, (0, 240))
    screen.blit(castle, (0, 345))
    #6 - Draw the screen elements
    mousepos = pygame.mouse.get_pos()
    angle = math.atan2(mousepos[1]-(playerpos[1]+32), mousepos[0]-(playerpos[0]+26))
    playerrot = pygame.transform.rotate(player, 360-angle/math.pi*180)
    blit_center(playerrot, playerpos)
    #6.2 - Draw arrows
    for bullet in arrows:
        index = 0
        velx = math.cos(bullet[0])*10
        vely = math.sin(bullet[0])*10
        bullet[1]+=velx
        bullet[2]+=vely
        if bullet[1]<-64 or bullet[1]>640 or bullet[2] <-64 or bullet[2]>480:
            arrows.pop(index)
        index += 1
        for projectile in arrows:
            arrow1 = pygame.transform.rotate(arrow, 360-projectile[0]/math.pi*180)
            screen.blit(arrow1, (projectile[1], projectile[2]))
    #6.3 - Draw badgers
    if badtimer == 0:
        badguys.append([640, random.randint(50, 430)])
        badtimer = 100 - (badtimer1*2)
        if badtimer1 >= 35:
            badtimer1 = 35
        else:
            badtimer1 += 5
    for index, badguy in enumerate(badguys):
        if badguy[0] < -64:
            badguys.pop(index)
            continue
        badguy[0] -= 7
        # 6.3.1 - Attack castle
        badrect = pygame.Rect(badguyimg.get_rect())
        badrect.top = badguy[1]
        badrect.left = badguy[0]
        if badrect.left < 64:
            healthvalue -= random.randint(5,20)
            badguys.pop(index)
            continue
        index1 = 0
        for bullet in arrows:
            arrownew = pygame.transform.rotate(arrow, 360-bullet[0]/math.pi*180)
            bullrect = pygame.Rect(arrownew.get_rect())
            bullrect.left = bullet[1]
            bullrect.top = bullet[2]
            if badrect.colliderect(bullrect):
                acc[0] += 1
                badguys.pop(index)
                arrows.pop(index1)
            index1 += 1
        # 6.3.3 - Next bad guy
    # 6.4 - Draw clock
    font = pygame.font.Font(None, 24)
    survivedtext = font.render(str((90000-pygame.time.get_ticks())/60000)+":"+str((90000-pygame.time.get_ticks())/1000%60).zfill(2), True, (0,0,0))
    textRect = survivedtext.get_rect()
    textRect.topright=[635,5]
    screen.blit(survivedtext, textRect)
    # 6.5 - Draw helth bar
    screen.blit(healthbar, (5, 5))
    for health1 in range(healthvalue):
        screen.blit(health, (health1+8, 8))

    for badguy in badguys:
        screen.blit(badguyimg, badguy)
    # playerpos1 = (playerpos[0]-playerrot.get_rect().width/2, playerpos[1]-playerrot.get_rect().height/2)
    # screen.blit(playerrot, playerpos1)
    #7 - Update the screen
    pygame.display.flip()
    #8 - Loop through the events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            for i, key in enumerate(arrawkeys):
                if event.key == key:
                    keys[i] = event.type == pygame.KEYDOWN
                    break
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                exit(0)
        if event.type == pygame.MOUSEBUTTONDOWN:
            position = pygame.mouse.get_pos()
            acc[1] += 1
            arrows.append([math.atan2(position[1]-(playerpos[1]),position[0]-(playerpos[0])),playerpos[0],playerpos[1]])
    #9 - Move player
    movestep = 5
    if keys[0] and playerpos[1]-player.get_height()/2 >= movestep:
        playerpos[1] -= movestep
    elif keys[2]  and playerpos[1] <= height-player.get_height()/2-movestep:
        playerpos[1] += movestep
    if keys[1] and playerpos[0]-player.get_width()/2 >= movestep:
        playerpos[0] -= movestep
    elif keys[3] and playerpos[0] <= width-player.get_width()/2-movestep:
        playerpos[0] += movestep


