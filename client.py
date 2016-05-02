import xmlrpclib

server = xmlrpclib.ServerProxy("http://localhost:8000")
clientId = server.create_game()
print server.start_game(clientId)

playing = True # Main loop control needed to break out of multiple levels

while playing:		
	print server.print_board(clientId)
	validMove = False
	while not validMove:
		reply = raw_input('\nMake your move: ')
		validMove = server.move_valid(clientId,reply)
	playing = server.make_move(clientId,reply)	

print server.print_board(clientId)
print server.print_result(clientId)
server.end_game(clientId)
