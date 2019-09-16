import copy
from collections import deque
#Setup starting position
# 8 6 7 
# 2 5 4 
# 3 0 1
# This position is 10 moves away from the desired position
#Desired position
# 1 2 3
# 4 5 6
# 7 8 0
board = [['0','5','2'],['1','4','3'],['7','8','6']]
des_board = [['1','2','3'],['4','5','6'],['7','8','0']]
x = len(board[0])
y = len(board)
heurstic = False

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
	print("Solved in ", len(bfs(board))," moves")

def bfs(start_node):
	visited = list()
	queue = deque([start_node])

	while len(queue) > 0:
		node = queue.pop()
		if parse_board(node) in visited:
			continue
		print_board(node)
		visited.append(parse_board(node))
		if parse_board(node) == parse_board(des_board):
			return visited

		for child in find_new_states(node):
			if parse_board(child) not in visited:
				queue.appendleft(child)
	return False

#Finds the possible new states of the board
def find_new_states(board_state_current,visited=[]):
	zero_pos = []
	#Find the position of 0
	for row in range(x):
		for col in range(y):
			if board_state_current[row][col] == "0":
				zero_pos = [row,col]
				break

	up,down,left,right = -1,-1,-1,-1
	#Look 4 ways, if a way goes beyond board limits it stays a -1
	if val_num(zero_pos[0]-1,x): #Because the board is always a square it doesn't matter wether x or y is the limit
		up = [zero_pos[0]-1,zero_pos[1]]

	if val_num(zero_pos[0]+1,x):
		down = [zero_pos[0]+1,zero_pos[1]]

	if val_num(zero_pos[1]-1,x):
		left = [zero_pos[0],zero_pos[1]-1]

	if val_num(zero_pos[1]+1,x):
		right = [zero_pos[0],zero_pos[1]+1]

	#For every way get the new board state if the number and 0 would be switched
	#If a way is invalid (-1) the state would be False
	state1 = switch_num(zero_pos,up,board_state_current)
	state2 = switch_num(zero_pos,down,board_state_current)
	state3 = switch_num(zero_pos,right,board_state_current)
	state4 = switch_num(zero_pos,left,board_state_current)


	#If a state is not False, add it to new_states
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
		successors = find_best_state(new_states)
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

#Parses the board to a string to be compared
def parse_board(board_state):
	board_str = ""
	for row in board_state:
		for num in row:
			board_str += num
	return board_str

#Checks the current state agains all the visited states to see if a dead-end is reached
def check_visited(new_state):
	for state in visited:
		if state == new_state:
			return False
	return True

def get_heurstic_value(c_board):
	current_board_num_dict = {}
	des_board_num_dict = {}
	for row in range(x):
		for col in range(y):
			current_board_num_dict[c_board[row][col]] = [row, col]
			des_board_num_dict[des_board[row][col]] = [row, col]
	total = 0
	for num in current_board_num_dict:
		row_pos = current_board_num_dict[num][0]
		col_pos = current_board_num_dict[num][1]

		des_row_pos = des_board_num_dict[num][0]
		des_col_pos = des_board_num_dict[num][1]

		hoz_moves = row_pos - des_row_pos
		ver_moves = col_pos - des_col_pos
		total += (abs(hoz_moves) + abs(ver_moves))
	return total
#Uses heurstic values to find the best ways
def find_best_state(board_states):
	best_h_val = -1
	options = []
	for board_state in board_states:
		h_val = get_heurstic_value(board_state)
		if best_h_val == -1:
			best_h_val = h_val
			options.append(board_state)

		elif h_val == best_h_val:
			best_h_val = h_val
			options.append(board_state)

		elif h_val < best_h_val:
			best_h_val = h_val
			options = []
			options.append(board_state)
	return options

program()