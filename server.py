# coding: utf-8
import time
from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

class ClientChannel(Channel):
	def __init__(self, *args, **kwargs):
		self.nickname = "anonymous"
		Channel.__init__(self, *args, **kwargs)

	def Close(self):
		print 'Client connection closed'

	def Network(self, data):
		print data

class GameServer(Server):
	channelClass = ClientChannel

	def __init__(self, *args, **kwargs):
		Server.__init__(self, *args, **kwargs)
		print 'Server launched'

	def Connected(self, channel, addr):
		print 'connected'

	def Launch(self):
		while True:
			self.Pump()
			time.sleep(0.001)

if __name__ == '__main__':
	server = GameServer(localaddr=("localhost", 12321))
	server.Launch()