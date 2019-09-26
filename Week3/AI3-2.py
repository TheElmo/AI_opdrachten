import itertools

def fill_board(A1,H1,V1,B1,A2,H2,V2,B2):
	board[A1] = "Aas"
	board[A2] = "Aas"
	board[H1] = "Heer"
	board[H2] = "Heer"
	board[V1] = "Vrouw"
	board[V2] = "Vrouw"
	board[B1] = "Boer"
	board[B2] = "Boer"


def not_neighbour_constraint(card1,card2,constraint):
	neigbours_list = neigbours[card1] + neigbours[card2]
	skip = False
	name_list = []
	for n in neigbours_list:
		name_list.append(board[n])
	if constraint in name_list:
		skip = True
	return skip

def all_neighbour_constraint(card,constraint):
	neigbours_list = neigbours[card]
	skip = False
	name_list = []
	for n in neigbours_list:
		name_list.append(board[n])
	if constraint not in name_list:
		skip = True
	return skip

def print_board(board):
	print("----- -----",board[0])
	print(board[1],board[2],board[3], "-----")
	print("-----",board[4],board[5],board[6])
	print("----- -----", board[7], "-----")

# - - 0 -
# 1 2 3 -
# - 4 5 6
# - - 7 -
positions = [0,1,2,3,4,5,6,7]
board = {0: None, 1:None, 2:None, 3: None, 4: None, 5: None, 6: None, 7:None}
neigbours = {0: [3], 1:[2],2:[4],3:[0,2,5],4:[2,5],5:[3,4,6,7],6:[5],7:[5]}
for (A1,H1,V1,B1,A2,H2,V2,B2) in list(itertools.permutations(positions)):
	fill_board(A1,H1,V1,B1,A2,H2,V2,B2)
	#C1
	if all_neighbour_constraint(A1,"Heer") and all_neighbour_constraint(A2,"Heer"):
		continue

	#C2
	if all_neighbour_constraint(H1,"Vrouw") and all_neighbour_constraint(H2,"Vrouw"):
		continue

	#C3
	if all_neighbour_constraint(V1,"Boer") and all_neighbour_constraint(V2,"Boer"):
		continue

	#C4
	if not_neighbour_constraint(A1,A2,"Vrouw"):
		continue

	#C5
	if not_neighbour_constraint(A1,A2,"Aas"):
		continue
	if not_neighbour_constraint(H1,H2,"Heer"):
		continue
	if not_neighbour_constraint(V1,V2,"Vrouw"):
		continue
	if not_neighbour_constraint(B1,B2,"Boer"):
		continue
	print_board(board)
	print()
	