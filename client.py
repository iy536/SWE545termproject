import xmlrpclib

server = xmlrpclib.ServerProxy("http://localhost:8000")
print server.init()

playing = True # Main loop control needed to break out of multiple levels

while playing:	
	try:
		print server.print_board()
		reply = raw_input('\nMake your move: ')
		playing = server.make_move(reply)
	except InvalidMove:
		server.invalid()
	except GameTied:
		server.print_board()
		server.game_tied()
		break
	except KeyboardInterrupt:
		server.game_over()
		break 
print server.print_board()
print server.print_result()
