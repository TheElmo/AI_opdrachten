import copy
from collections import deque
#Setup starting position (Randomly choosen)
# 0 5 2
# 1 4 3 
# 7 8 6

# This position is 10 moves away from the desired position
#Desired position
# 1 2 3
# 4 5 6
# 7 8 0

#Some more test cases
#board = [['0','5','2'],['1','4','3'],['7','8','6']]
#board = [['2','4','0'],['1','6','3'],['7','5','8']]
board = [['2','4','3'],['1','5','6'],['0','7','8']]
#board = [['2','0','3'],['1','4','5'],['7','8','6']]

des_board = [['1','2','3'],['4','5','6'],['7','8','0']]
x = len(board[0])
y = len(board)
heurstic = False

#Small function that prints the board in an easy readable format
def print_board(board_to_print):
	#Print board
	for row in board_to_print:
		row_string = ""
		for num in row:
			row_string += num + " "
		print(row_string)
	print("---")

#This program is tested with the board above, but it should work on any N*N board
def program():
	res = bfs(board)
	if res[0]:
		print("Solved in ", len(res[1])," moves")
	else:
		print("Could not solve this board")

#Basic BFS algorithm, adds children of a node (board state) to the left (start) of a queue and pops off a new node from the right (end) of the queue, bassicly it works like a pipeline
def bfs(start_node):
	visited = []
	queue = deque([start_node])

	while len(queue) > 0:
		#print(queue)
		node = queue.pop()
		if parse_board(node) in visited:
			continue
		print_board(node)
		visited.append(parse_board(node))
		if parse_board(node) == parse_board(des_board):
			return [True,visited]
		for child in find_new_states(node, visited):
			if parse_board(child) not in visited:
				queue.appendleft(child)
	return [False]
#Finds the possible new states of the board, if heuristic is turned on (True) it will also choose the best new state conform the find_best_state() function
def find_new_states(board_state_current,visited=[]):
	zero_pos = []
	#Find the position of 0
	for row in range(x):
		for col in range(y):
			if board_state_current[row][col] == "0":
				zero_pos = [row,col]
				break

	up,down,left,right = -1,-1,-1,-1
	#Look 4 directions, if a direction goes beyond board limits it stays a -1
	if val_num(zero_pos[0]-1,x): #Because the board is always a square it doesn't matter wether x or y is the limit
		up = [zero_pos[0]-1,zero_pos[1]]

	if val_num(zero_pos[0]+1,x):
		down = [zero_pos[0]+1,zero_pos[1]]

	if val_num(zero_pos[1]-1,x):
		left = [zero_pos[0],zero_pos[1]-1]

	if val_num(zero_pos[1]+1,x):
		right = [zero_pos[0],zero_pos[1]+1]

	#For every direction; get the new board state if the number and 0 would be switched (sliding over the number to the empty spot)
	#If a direction is invalid (-1) the state would be False
	state1 = switch_num(zero_pos,up,board_state_current)
	state2 = switch_num(zero_pos,down,board_state_current)
	state3 = switch_num(zero_pos,right,board_state_current)
	state4 = switch_num(zero_pos,left,board_state_current)

	#If a state is not False (valid) and it hasn't been visited yet, add it to new_states
	new_states = []
	if state1 and parse_board(state1) not in visited:
		new_states.append(state1)
	if state2 and parse_board(state2) not in visited:
		new_states.append(state2)
	if state3 and parse_board(state3) not in visited:
		new_states.append(state3)
	if state4 and parse_board(state4) not in visited:
		new_states.append(state4)
	if heurstic: 
		successors = find_best_state(new_states) #If heuristic is True, give the list of children to the find_best_state function that will return a list of best options
	else: 
		successors = new_states.copy()
	return successors

#Switches the 0 with an adjecent number on the board (sliding)
def switch_num(zero_pos,num_pos,old_board):
	if num_pos == -1: #This pos is not valid
		return False
	new_board = copy.deepcopy(old_board)
	temp = old_board[zero_pos[0]][zero_pos[1]]
	new_board[zero_pos[0]][zero_pos[1]] = old_board[num_pos[0]][num_pos[1]] #Put the number in the 0 position
	new_board[num_pos[0]][num_pos[1]] = temp #Put the 0 in the number position
	return new_board

#Validates wether a number is inside the board limits
def val_num(num, lim):
	if num < 0:
		return False
	elif num == lim:
		return False
	return True

#Parses the board to a string to be compared with other board states
def parse_board(board_state):
	board_str = ""
	for row in board_state:
		for num in row:
			board_str += num
	return board_str

#Gets the total score of a board, the score is calculated by taking the sum of the number of moves each number has to make to get to his desired spot
def get_heurstic_value(c_board):
	current_board_num_dict = {}
	des_board_num_dict = {}

	#Fill the 2 dicts (current board and desired board) with each number as a key and their position on the board as value
	for row in range(x):
		for col in range(y):
			current_board_num_dict[c_board[row][col]] = [row, col]
			des_board_num_dict[des_board[row][col]] = [row, col]

	total = 0

	#Calculate the sum of all moves each number needs to reach it desired spot
	for num in current_board_num_dict:
		row_pos = current_board_num_dict[num][0]
		col_pos = current_board_num_dict[num][1]

		des_row_pos = des_board_num_dict[num][0]
		des_col_pos = des_board_num_dict[num][1]

		hoz_moves = row_pos - des_row_pos
		ver_moves = col_pos - des_col_pos
		total += (abs(hoz_moves) + abs(ver_moves))
	return total

#Uses the heuristic value from get_heurstic_value to check to best posible option from all its choices
def find_best_state(board_states):
	best_h_val = -1
	options = []
	for board_state in board_states:
		h_val = get_heurstic_value(board_state)
		if best_h_val == -1:
			best_h_val = h_val
			options.append(board_state)

		elif h_val == best_h_val: #If a board state is equaly good as the current option it is also added to the list of options
			best_h_val = h_val
			options.append(board_state)

		elif h_val < best_h_val:
			best_h_val = h_val
			options = []
			options.append(board_state)

	#Add the rest of the options add the back
	# for board_state in board_states:
	# 	if board_state not in options:
	# 		options.append(board_state)
	return options

program()