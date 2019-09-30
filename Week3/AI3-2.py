import itertools

#Vult het board dictionary door een string te zetten als value van een key (key stelt een kaart voor: A1 is de eerste aas, A2 is de tweede aas enz...)
def fill_board(A1,H1,V1,B1,A2,H2,V2,B2):
	board[A1] = "Aas"
	board[A2] = "Aas"
	board[H1] = "Heer"
	board[H2] = "Heer"
	board[V1] = "Vrouw"
	board[V2] = "Vrouw"
	board[B1] = "Boer"
	board[B2] = "Boer"

#Checked of een gegeven kaart (constraint) voorkomt in de gezamenlijke burenlijst van kaart 1 (card1) en kaart 2 (card2), 
# als dit zo is wordt True teruggegeven wat aangeeft dat dit geen goede oplossing is en geskiped moet worden
def constraint_not_neighbour(card1,card2,constraint):
	neigbours_list = neigbours[card1] + neigbours[card2]
	skip = False
	neighbours_card_list = []
	for neighbour in neigbours_list:
		neighbours_card_list.append(board[neighbour])
	if constraint in neighbours_card_list:
		skip = True
	#Skipt waarneer de constraint wel voorkomt in de (gezamelijke) burenlijst( De constraint moet dus niet voorkomen)
	return skip

#Checked of een gegeven kaart (constraint) voorkomt in de burenlijst van een kaart (card),
# als dit NIET zo is wordt True teruggegeven wat aangeeft dat dit geen goede oplossing is en geskiped moet worden
def constraint_is_neighbour(card,constraint):
	neigbours_list = neigbours[card]
	skip = False
	neighbours_card_list = []
	for neighbour in neigbours_list:
		neighbours_card_list.append(board[neighbour])
	if constraint not in neighbours_card_list:
		skip = True
	#Skipt waarneer de constraint niet voorkomt in burenlijst (De constraint moet dus voorkomen in de burenlijst)
	return skip

# Checked of het hele boord gevuld, als dit zo is wordt True teruggegeven, anders False
def is_board_filled(board):
	for card in board.keys():
		if board[card] == None:
			return False
	return True

#Print het spelboord met de kaarten op hun juiste locatie
def print_board(board):
	print("----- -----",board[0])
	print(board[1],board[2],board[3], "-----")
	print("-----",board[4],board[5],board[6])
	print("----- -----", board[7], "-----")

# - - 0 -
# 1 2 3 -
# - 4 5 6
# - - 7 -
positions = [0,1,2,3,4,5,6,7]# de 8 posities van de kaarten
board = {0: None, 1:None, 2:None, 3: None, 4: None, 5: None, 6: None, 7:None} #Het spelboord, elke positie is een key, elke kaart is de value
neigbours = {0: [3], 1:[2],2:[4],3:[0,2,5],4:[2,5],5:[3,4,6,7],6:[5],7:[5]} #Een dictionary van buren waarbij de key een positie is en de value een tuple van grenzende posities

def brute_force():
	solutions = []
	for (A1,H1,V1,B1,A2,H2,V2,B2) in list(itertools.permutations(positions)):
		fill_board(A1,H1,V1,B1,A2,H2,V2,B2)
		#Constraint: elke aas grenst aan een heer
		if constraint_is_neighbour(A1,"Heer") or constraint_is_neighbour(A2,"Heer"):
			continue
		#Constraint: elke heer grenst aan een vrouw
		if constraint_is_neighbour(H1,"Vrouw") or constraint_is_neighbour(H2,"Vrouw"):
			continue

		#Constraint: elke vrouw grenst aan een boer
		if constraint_is_neighbour(V1,"Boer") or constraint_is_neighbour(V2,"Boer"):
			continue

		#Constraint: elke aas grenst NIET aan een vrouw
		if constraint_not_neighbour(A1,A2,"Vrouw"):
			continue

		#Constraint: 2 dezelfde kaarten mogen niet grenzen
		if constraint_not_neighbour(A1,A2,"Aas"):
			continue
		if constraint_not_neighbour(H1,H2,"Heer"):
			continue
		if constraint_not_neighbour(V1,V2,"Vrouw"):
			continue
		if constraint_not_neighbour(B1,B2,"Boer"):
			continue

		#Oplossing al gevonden met omgekeerde kaarten, b1 <= => b2
		if board in solutions:
			continue
		solutions.append(board)
		print_board(board)

#Vind de keys (positities) van alle kaarten op het boord en stuurt deze als lijst terug
def find_board_keys(board):
	ace_keys = []
	jack_keys = []
	king_keys = []
	queen_keys = []
	for position in board:
		if board[position] == "Aas":
			ace_keys.append(position)
		if board[position] == "Heer":
			king_keys.append(position)
		if board[position] == "Vrouw":
			queen_keys.append(position)
		if board[position] == "Boer":
			jack_keys.append(position)
	A1,A2 = ace_keys[0], ace_keys[1]
	H1,H2 = king_keys[0], king_keys[1]
	V1,V2 = queen_keys[0], queen_keys[1]
	B1,B2 = jack_keys[0], jack_keys[1]
	return [A1,A2,H1,H2,V1,V2,B1,B2]

#Check of een boord alle constraints doorstaat, zo ja True anders False
def is_valid(board):
	#Constraint: het boord moet gevuld zijn
	if not is_board_filled(board):
		return False

	keys = find_board_keys(board)
	A1,A2 = keys[0],keys[1]
	H1,H2 = keys[2],keys[3]
	V1,V2 = keys[4],keys[5]
	B1,B2 = keys[6],keys[7]

	if constraint_is_neighbour(A1,"Heer") or constraint_is_neighbour(A2,"Heer"):
		return False
	#Constraint: elke heer grenst aan een vrouw
	if constraint_is_neighbour(H1,"Vrouw") or constraint_is_neighbour(H2,"Vrouw"):
		return False
	#Constraint: elke vrouw grenst aan een boer
	if constraint_is_neighbour(V1,"Boer") or constraint_is_neighbour(V2,"Boer"):
		return False
	#Constraint: elke aas grenst NIET aan een vrouw
	if constraint_not_neighbour(A1,A2,"Vrouw"):
		return False
	#Constraint: 2 dezelfde kaarten mogen niet grenzen
	if constraint_not_neighbour(A1,A2,"Aas"):
		return False
	if constraint_not_neighbour(H1,H2,"Heer"):
		return False
	if constraint_not_neighbour(V1,V2,"Vrouw"):
		return False
	if constraint_not_neighbour(B1,B2,"Boer"):
		return False
	return True

# De kaarten die nog neergelegd kunnen worden
domain = ["Aas","Aas","Heer","Heer","Vrouw","Vrouw","Boer","Boer"]
def dfs(board,key=0):
	print(board)
	if is_valid(board):
		print_board(board)
		return True
	for value in domain:
		board[key] = value
		domain.remove(value)
		if dfs(board,key+1):
			return True
		domain.append(value)
		board[key] = None
	return False


#brute_force()
dfs(board)