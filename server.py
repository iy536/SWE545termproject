
from SimpleXMLRPCServer import SimpleXMLRPCServer
from tic_tac_toe.game import Game

import sys
import os
import random

game = Game(3)

QUIT_STRINGS = ['quit', 'exit', 'bye']

class TicTacToe:
	def _print_file(self, filename):
	  try:
		f = open(filename, "r")
		try:
		  string = f.read()
		  return string
		finally:
		  f.close()
	  except IOError:
		pass
	def init(self):
	  os.system('clear')	  
	  print self._print_file('images/banner.txt')
	  print 'Please make your move by entering a number from the movement key.'
	  print "Type '%s' to exit the game." % QUIT_STRINGS[0]
	  result = self._print_file('images/banner.txt')
	  result += 'Please make your move by entering a number from the movement key.\n'
	  result += "Type '%s' to exit the game." % QUIT_STRINGS[0]
	  return result

	def game_over(self):	  
	  return self._print_file('images/game_over.txt')

	def winner(self):
	  return self._print_file('images/winner.txt')

	def loser(self):
	  return self._print_file('images/loser.txt')

	def game_tied(self):
	  return self._print_file('images/game_tied.txt')
	def invalid(self):
	  print "Invalid move. Please use the movement key or type '%s'." % QUIT_STRINGS[0]
	def make_move(self, reply): 	  
	  playing = True
	  game.make_move(reply, 'X')
	  if not game.check_winner('X'):
		game.make_move(random.choice(game.valid_moves()),'O')
		if game.check_winner('O'):
			playing = False
	  else:
		playing = False
	  return playing 
	
	def print_result(self):	
		if game.check_winner('X'):
			return self.winner()
		if game.check_winner('O'):
			return self.loser()
		else:
			self.game_tied()
			
	def print_board(self):
	  result = '\nBoard:%sMovement Key:\n' % (' '*(2 * game.size + 9))
	  for y in list(range(game.size)):
		row = ''
		for x in list(range(game.size)):
		  if x != 0:
			row += '|'
		  row += '%1s' % game.board[y][x]
		row += ' '*16
		for x in list(range(game.size)):
		  if x != 0:
			row += '|'
		  string = '%' + str(len(str(game.size ** 2))) + 'd'
		  row += string % (y * game.size + x + 1)
		result += row
		result +='\n'
	  return result
				
server = SimpleXMLRPCServer(("localhost",8000), allow_none=True)
server.register_introspection_functions()

server.register_instance(TicTacToe())
server.serve_forever()