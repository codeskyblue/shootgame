# coding: utf-8
import time
import pygame
import math
import weakref
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class Player(pygame.Surface):
    def __init__(self, nickname='anonymous'):
        self.nickname = nickname
        self.pos = (100, 100)
        self.dest = (200, 200)
        self.speed = 2
        self.angle = 0
        self.uptick = None

    def __str__(self):
        return 'Name: %s' % (self.nickname)

    def update(self, ticks):
        ''' 
        Should call in every tick
        Control player move
        '''
        if self.uptick == None:
            self.uptick = ticks
        cx, cy = self.pos
        dx, dy = self.dest
        if abs(cx-dx) > 5 or abs(cy-dy) > 5:
            radius = math.atan2(dy-cy, dx-cx)
            self.angle = 360-radius/math.pi*180
            #self.player = pygame.transform.rotate(self.player, 360-angle/math.pi*180)
            t = ticks - self.uptick
            print t
            self.uptick = ticks
            nx = cx + math.cos(radius)*self.speed*t
            ny = cy + math.sin(radius)*self.speed*t
            self.pos = [nx, ny]
            #self.Send({'action': 'postion', 'position': self.pos})

    def dumps(self):
        return {
            'pos': self.pos,
            'dest': self.dest
        }

class PvPGame():
    def __init__(self, gameid, players):
        self.gameid = gameid
        # self.player0 = players[0]
        # self.player1 = players[1]
        self.players = players

    def update(self):
    	# for player in self.players:
    	# 	self.
        self.player0.Send({'action': 'selfpos', 'position': self.player0.dumps()})
        self.player1.Send({'action': 'selfpos', 'position': self.player0.dumps()})

class ClientChannel(Channel):
    def __init__(self, *args, **kwargs):
        self.nickname = "anonymous"
        Channel.__init__(self, *args, **kwargs)

    def Close(self):
        print 'Client connection closed'
        self._server.DelPlayer(self)

    @property
    def player(self):
         return self._server.players[self]

    def Network(self, data):
        print data

    def Network_playerdest(self, data):
        print data, self.player
        self.player.dest = data['dest']

    def Network_ping(self, data):
        print data
        self.Send({'action': 'pong', 'timestamp': data['timestamp']})


class GameServer(Server):
    channelClass = ClientChannel

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.players = weakref.WeakKeyDictionary()
        self.pvpgames = []
        print 'Server launched'

    def Connected(self, channel, addr):
        print 'connected: ' + str(addr)
        self.AddPlayer(channel)

    def AddPlayer(self, channel):
        self.players[channel] = Player()

    def DelPlayer(self, channel):
        print 'Del player:' + str(channel.addr)
        del self.players[channel]

    def Tick(self):
    	ticks = pygame.time.get_ticks()
        for channel, player in self.players.items():
            player.update(ticks)
            channel.Send({'action': 'postion', 'position': player.dumps()})

    def Launch(self):
        while True:
            self.Tick()
            self.Pump()
            time.sleep(0.001)

if __name__ == '__main__':
    server = GameServer(localaddr=("localhost", 12321))
    server.Launch()