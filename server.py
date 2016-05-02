from tic_tac_toe.game import Game
from SimpleXMLRPCServer import SimpleXMLRPCServer

import sys
import os
import random
import threading

QUIT_STRINGS = ['quit', 'exit', 'bye']

class InvalidMove(Exception):
  pass
	
class TicTacToeThread(threading.Thread):
	def __init__(self,game):
		self.game = game
		threading.Thread.__init__(self)	
		
	def start_game(self):	  
	  result = self.print_file('images/banner.txt')
	  result += 'Please make your move by entering a number from the movement key.\n'
	  result += "Type '%s' to exit the game." % QUIT_STRINGS[0]
	  return result
	
	def print_file(self, filename):
	  try:
		f = open(filename, "r")
		try:
		  string = f.read()
		  return string
		finally:
		  f.close()
	  except IOError:
		pass
		
	def print_board(self):
	  result = '\nBoard:%sMovement Key:\n' % (' '*(2 * self.game.size + 9))
	  for y in list(range(self.game.size)):
		row = ''
		for x in list(range(self.game.size)):
		  if x != 0:
			row += '|'
		  row += '%1s' % self.game.board[y][x]
		row += ' '*16
		for x in list(range(self.game.size)):
		  if x != 0:
			row += '|'
		  string = '%' + str(len(str(self.game.size ** 2))) + 'd'
		  row += string % (y * self.game.size + x + 1)
		result += row
		result +='\n'
	  return result
	  
	def make_move(self, reply, symbol):
		self.game.make_move(reply,symbol)
	
	def move_valid(self, reply):	
		if int(reply) in self.game.valid_moves():
			print 'Valid move'
			return True
		else:
			print 'InValid move'
			return False
		
	def check_winner(self, symbol):
		return self.game.check_winner(symbol)
		
	def valid_moves(self):
		return self.game.valid_moves()
		
	def print_result(self):
		if self.game.check_winner('X'):
			return self.winner()
		if self.game.check_winner('O'):
			return self.loser()
		else:
			return self.game_tied()
			
	def game_over(self):	  
	  return self.print_file('images/game_over.txt')

	def winner(self):
	  return self.print_file('images/winner.txt')

	def loser(self):
	  return self.print_file('images/loser.txt')

	def game_tied(self):
	  return self.print_file('images/game_tied.txt')
	  
	def invalid(self):
	  print "Invalid move. Please use the movement key or type '%s'." % QUIT_STRINGS[0]

class TicTacToeGame():
	def __init__(self):
		self.clientMapping = {}
		self.clientId = 0
		
	def create_game(self):	
		game = Game(3)
		thread = TicTacToeThread(game)
		clientId = self.clientId
		self.clientId += 1
		self.clientMapping[clientId] = thread
		thread.start()
		return clientId
		
	def start_game(self,clientId):
		thread = self.clientMapping[clientId]
		return thread.start_game()
		
	def end_game(self,clientId):
		thread = self.clientMapping[clientId]
		thread.join()
		
	def print_board(self,clientId):
	  thread = self.clientMapping[clientId]
	  return thread.print_board()
	  
	def move_valid(self, clientId, reply):  
		thread = self.clientMapping[clientId]
		return thread.move_valid(reply)
	  
	def make_move(self, clientId, reply):
	  thread = self.clientMapping[clientId]
	  thread.make_move(reply, 'X')
	  playing = True	  
	  if not thread.check_winner('X'):		
		thread.make_move(random.choice(thread.valid_moves()),'O')
		if thread.check_winner('O'):
			playing = False
	  else:
		playing = False
	  return playing 
	
	def print_result(self,clientId):	
		thread = self.clientMapping[clientId]
		return thread.print_result()
				    			
server = SimpleXMLRPCServer(("localhost", 8000), allow_none=True)
server.register_introspection_functions()
server.register_instance(TicTacToeGame())
server.serve_forever()