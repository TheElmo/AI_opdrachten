import random
import itertools
import math
import copy

MAX_DEPTH = 3
def merge_left(b):
    # merge the board left
    # this is the funcyoin that is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row, acc):
        # recursive helper for merge_left

        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accumulator
        if len(row) == 1:
            return acc + [x]

        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accumulator, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accumulator, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b):
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x):
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]


def merge_up(b):
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]


def merge_down(b):
    # merge the board downward
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[0, 0, 0, 2], [0, 0, 2, 4], [0, 0, 8, 2], [4, 8, 4, 2]]
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]


# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b):
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b):
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                if x == y or x == 0 or y == 0:
                    return True
        return False

    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start():
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b


def play_move(b, direction):
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b


def add_two_four(b):
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, rows):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue

def game_state(b):
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [(2, 4, 8, 4), (0, 2, 2, 8), (0, 0, 0, 4), (0, 0, 0, 2)]
    assert merge_down(b) == [(0, 0, 0, 4), (0, 0, 0, 8), (0, 2, 8, 4), (2, 4, 2, 2)]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [(2, 8, 4, 0), (16, 0, 2, 0), (4, 0, 0, 0), (0, 0, 0, 0)]
    assert (merge_down(b)) == [(0, 0, 0, 0), (2, 0, 0, 0), (16, 0, 4, 0), (4, 8, 2, 0)]
    assert (move_exists(b)) == True
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    g = Game()
    for i in range(11):
        g.add_two_four(b)

def get_random_move():
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def compare(A, B):
    stringA = combine_rows(A)
    stringB = combine_rows(B)
    return stringA == stringB

def combine_rows(board):
    row_string = ''
    for row in board:
        for num in row:
            row_string += str(num)
    return row_string

def get_new_board(direction,board):
    temp_board= copy.deepcopy(board)
    return play_move(temp_board,direction)


def get_children(b):
    board_left,board_up,board_right,board_down = None,None,None,None
    children = []
    for direction in list(MERGE_FUNCTIONS.keys()):
        new_board = get_new_board(direction, b)
        if new_board != None:
            children.append((new_board,direction))
    return children

def get_expectimax_move(b):
    best_move = ""
    best_value = 0
    for child in get_children(b):
        result = expectimax(b)
        if result[1] > best_value:
            best_value = result[1]
            best_move = result[0]
    return best_move

def expectimax(b,depth=MAX_DEPTH,move_made=None):
    if game_state(b) == "win" or depth == 0:
        return (move_made,get_heuristic_board_value(move_made,b))
    branch_total = 0
    best_move = ""
    best_value = 0
    children = get_children(b)
    for child in children:
        result = expectimax(b,depth-1,child[1])
        if result[1] > best_value:
            best_value = result[1]
            best_move = result[0]
        branch_total += result[1]
    return (best_move,branch_total/len(children))

def check_highest_value_location(b):
    #Checks if location is top left corner
    highest_value_location = [0,0]
    highest_value = 0
    for row in range(4):
        for col in range(4):
            val = b[row][col]
            if val > highest_value:
                highest_value = val
                highest_value_location[0] = row
                highest_value_location[1] = col
    if highest_value_location[0] == 0 and highest_value_location[1] == 0:
        return 30
    return 0

def get_row_sum(row,b):
    row_sum = 0
    for col in range(4):
        row_sum += b[row][col]
    return row_sum


def get_board_score(board):
    zero_count = 0
    for row in board:
        for num in row:
            if num == 0:
                zero_count += 1
    return (3*check_cols(board)) + zero_count + check_highest_value_location(board) + (2.5*get_row_sum(0,board)) + (2 * get_row_sum(1,board)) + (1.5 * get_row_sum(2,board)) + get_row_sum(3,board)

def get_heuristic_board_value(direction,b):
    return get_board_score(play_move(b,direction))

def check_cols(b):
    valid_cols = []
    for index in range(4):
        col_values = []
        for row in b:
            col_values.append(row[index])
        #col_values is now a list of all values in one column
        valid_cols.extend(check_line(index, col_values))
    return len(valid_cols)

def check_line(index, values):
    valid_lines = []
    has_partner = False
    for compare_index in range(3):
        compare_index +=1 #Skip the 0 and go until 3
        if values[compare_index] == 0 and compare_index != 3: #If current tile is empty skip to next, but only if it is not the last tile in the row
            continue 
        if compare_index == index:
            continue
        if values[index] == values[compare_index] and values[index] != 0:
            #If there is atleast one tile in the col_values with the same value it has a partner
            has_partner = True
        if values[index] == values[compare_index] or values[compare_index] == 0:
            #If it has reached the end, is still valid and the col_values contains uninterupted partners it is a valid row
            if compare_index == 3 and has_partner:
                valid_lines.append(values)
        else:
            break
    return valid_lines