"""
Tic Tac Toe Player
"""

import math
import copy 
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    turn = 0
    for row in board:
        for cell in row:
            if cell is not EMPTY:
                turn += 1
    if turn % 2 == 0:
        return X
    return O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] is EMPTY:
                actions.add((i,j))
    return actions

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    i = action[0]
    j = action[1]
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    win = None


    for i in range(len(board)):
        if board[i][0] == board[i][1] == board[i][2]:
            win = board[i][0]
        if board[0][i] == board[1][i] == board[2][i]:
            win = board[0][i]

    if board[0][0] == board[1][1] == board[2][2]:
        win = board[0][0]
    if board[0][2] == board[1][1] == board[2][0]:
        win = board[0][2]



    return win

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        for cell in row:
            if cell is EMPTY:
                return False
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def max_value(board):
    if terminal(board):
        return (utility(board))
    else:
        v = -math.inf
        for action in actions(board):
            v = max(v,min_value(result(board,action)))
        return v

def min_value(board):
    if terminal(board):
        return utility(board)
    else:
        v = math.inf
        for action in actions(board):
            v = min(v,max_value(result(board,action)))
        return v

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    optimal_move = None
    current_player = player(board)
    
    if current_player == X:
        if board == initial_state():
            return (1,1)
        best_score = -math.inf
        for action in actions(board):
            eval_score = min_value(result(board,action))
            if eval_score > best_score:
                optimal_move = action
                best_score = eval_score 
    else:
        best_score = math.inf
        for action in actions(board):
            eval_score = max_value(result(board,action))
            if eval_score < best_score:
                optimal_move = action
                best_score = eval_score 

    return optimal_move
   