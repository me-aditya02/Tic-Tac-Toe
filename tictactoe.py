import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}

def result(board, action):
    if action not in actions(board):
        raise ValueError("Invalid action")
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board

def winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not EMPTY:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not EMPTY:
        return board[0][2]
    return None

def terminal(board):
    return winner(board) is not None or all(cell is not EMPTY for row in board for cell in row)

def utility(board):
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    return 0

def minimax(board):
    if terminal(board):
        return None
    
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = -math.inf
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v
    
    def min_value(board):
        if terminal(board):
            return utility(board)
        v = math.inf
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v
    
    best_action = None
    if player(board) == X:
        best_val = -math.inf
        for action in actions(board):
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best_action = action
    else:
        best_val = math.inf
        for action in actions(board):
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best_action = action
    
    return best_action

def print_board(board):
    for row in board:
        print(" ".join([cell if cell else "-" for cell in row]))
    print()

def play_game():
    board = initial_state()
    while not terminal(board):
        print_board(board)
        if player(board) == X:
            while True:
                try:
                    i, j = map(int, input("Enter your move (row and column 0-2): ").split())
                    if (i, j) in actions(board):
                        break
                    else:
                        print("Invalid move, try again.")
                except ValueError:
                    print("Invalid input, enter two numbers between 0 and 2.")
        else:
            (i, j) = minimax(board)
            print(f"AI chooses: {i} {j}")
        board = result(board, (i, j))
    
    print_board(board)
    if winner(board):
        print(f"Winner: {winner(board)}")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    play_game()