#setup board
# S R E G M I
# A T E N G N
# O U T A X I
# M I S T A N
# J T A R G I
# Q A R C E T

#Every letter on the board has a position consisting of a row and a col, f.e. the 's' in the top left has row=0,col=0. The 't' in the bottom right has row=5,col=5
board = [['s','r','e','g','m','i'],['a','t','e','n','g','n'],['o','u','t','a','x','i'],['m','i','s','t','a','n'],['j','t','a','r','g','i'],['q','a','r','c','e','t']]
x = len(board)
y = len(board[0])
#Words to find: Mist, Mis, Misten, Tang, Target, Taxi, Tart
words = ['mist','mis','misten','tang','target','taxi','tart']
#Define Solutions
#Here are the solutions for the 7 testwords on this board that we intended (There could be more solutions found by the program)
sol = {'mist': [[3,0],[3,1],[3,2],[3,3]],
	   'misten': [[3,0],[3,1],[3,2],[2,2],[1,2],[1,3]],
	   'mis': [[0,4],[0,5],[0,0]],
	   'tang': [[1,1],[1,0],[1,5],[1,4]],
	   'target': [[4,1],[4,2],[4,3],[4,4],[5,4],[5,5]],
	   'taxi': [[2,2],[2,3],[2,4],[2,5]],
	   'tart': [[4,1],[5,1],[0,1],[1,1]]}

#Print board, don't think this is to complicated
for row in board:
	row_string = ""
	for letter in row:
		row_string += letter + " "
	print(row_string)

#The program is tested on the board (with the words) defined above. 
#But it can function on any board of any N*N size, if a word has multiple solutions (it exists multiple times) all solutions will be printen
def program(board, words):
	print("The board is ", x ," by ", y)

	for word in words:
		find(board, word)

def find(board, word):
	#Find the position of the first letter of the word (there could be multiple!, if first letter=t every t on the board is an option)
	letter = word[0]
	for row in range(x):
		for col in range(y):
			if(board[row][col] == letter):
				check_letter(row,col,word,1,[]) #When a position is found, start the proces of checking that letter

def check_letter(row,col,word,i,solut):
	solut.append([row,col]) #First append the (possible) solution step to a list
	if len(word) == i: #Check if we've reached the length of the word (this indicates that we would have found the word)
		print("The solution for '" +word+ "' is: ",solut)
		del solut[-1] #go back one step to try for more solutions, You never know ;)
		return True #Indicates the word has been found
	valid_ways = check_around([row,col],word[i])
	if len(valid_ways) == 0: #If there are no valid ways we have reached a dead-end
		return False
	if len(valid_ways) != 0: #If there are valid sollutions move the pointer on the word to the next letter
		i+=1
	for way in valid_ways: #Check every way of valid ways
		if check_letter(way[0],way[1],word,i,solut): #A possible is used as new input in the same function, if True is returned we have found the word 
			return
		else: #If False has returned we have found a dead end and need to remove the possible solution entry
			del solut[-1]

def check_around(position,check_for):
	valid_ways = []

	#Get the positions of all four ways, If we go right of the board we enter the same row on the left, same if we go to far up we enter the same column at the bottom (This is done by the val_num function)
	up = [val_num(position[0]-1,y), val_num(position[1],x)]
	down = [val_num(position[0]+1,y), val_num(position[1],x)]
	left = [val_num(position[0],y),val_num(position[1]-1,x)]
	right = [val_num(position[0],y),val_num(position[1]+1,x)]

	#If any of the four new positions contains the letter we are looking for it is added to valid_ways
	if board[left[0]][left[1]] == check_for:
		valid_ways.append([left[0],left[1]])

	if board[right[0]][right[1]] == check_for:
		valid_ways.append([right[0],right[1]])

	if board[up[0]][up[1]] == check_for:
		valid_ways.append([up[0],up[1]])

	if board[down[0]][down[1]] == check_for:
		valid_ways.append([down[0],down[1]])
	return valid_ways

def val_num(num,a):
	#Makes sure we stay within the board
	if num >= a:
		num = num - a
	if num < 0:
		num = num + a
	return num
program(board,words)


#CODE VAN DUO JELMER&WOUTER