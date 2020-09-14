"""
Tic Tac Toe Player
"""

import math
import copy


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class Tree():
    def __init__(self, root=None):
        self.root = root

    def change_root(self, node):
        self.root = node


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
    counterX = counterO = 0

    for row in board:
        counterX += row.count(X)
        counterO += row.count(O)

    return O if counterO < counterX else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i, row in enumerate(board):
        for j, column in enumerate(row):
            if column == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if(not (0 <= i < 3 and 0 <= j < 3)):
        raise("invalid action for the board")

    plyr = player(board)
    copyBoard = copy.deepcopy(board)

    copyBoard[i][j] = plyr
    return copyBoard


def all_Equals(lst):
    """
    Returns None if any element is different in the list, or if all the elements are equals return the element
    """
    for i in lst:
        if lst[0] != i:
            return None
    return lst[0]


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Diagonal possibilities to win
    result = all_Equals([board[i][i] for i in range(3)])
    if(result is None):
        result = all_Equals([board[i][2-i] for i in range(3)])

    # Horizontal and Vertical possibilities to win
    for i in range(3):
        if result is None:
            result = all_Equals([row[i] for row in board])
        if result is None:
            result = all_Equals(board[i][:])

    return result


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if(winner(board) is not None):
        return True

    for row in board:
        for column in row:
            if column is None:
                return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winnr = winner(board)
    if(winnr == X):
        return 1
    elif(winnr == O):
        return -1
    else:
        return 0


def min_value(board, alpha, beta):
    if terminal(board):
        return ((0, 0), utility(board))

    v = math.inf
    bestAction = None

    for action in actions(board):
        nextAction, nextV = max_value(result(board, action), alpha, beta)
        if(nextV < v):
            v = nextV
            bestAction = action
        alpha = min(beta, nextV)
        if beta <= alpha:
            break

    return (bestAction, v)


def max_value(board, alpha, beta):
    if terminal(board):
        return ((0, 0), utility(board))

    v = -math.inf
    bestAction = None

    for action in actions(board):
        nextAction, nextV = min_value(result(board, action), alpha, beta)
        if(nextV > v):
            v = nextV
            bestAction = action
        alpha = max(alpha, nextV)
        if beta <= alpha:
            break
        
    return (bestAction, v)


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if(player(board) == X):
        nextAction, nextV = max_value(board, -math.inf, math.inf)
    else:
        nextAction, nextV = min_value(board, -math.inf, math.inf)
    return nextAction
