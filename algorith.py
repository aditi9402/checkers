from copy import deepcopy #a deepcopy copies the reference as well as the object 
import pygame

#deepcopy:
# x=[]
# y=deepcopy(x)
# If we modify x, it won't modify y(and vice versa) here.

RED = (255,0,0)
WHITE = (255, 255, 255) 
def minimax(state, depth, alpha, beta, max_player, game):
    if depth == 0 or state.winner() is not None:
        return state.evaluate(), state #state: return state of checker_brd
    
    if max_player:
        maxEval = float('-inf') #fetch
        best_move = None
        for move in fetch_all_moves(state, WHITE, game):
            evaluation = minimax(move, depth-1, alpha, beta, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
            alpha = max(alpha, maxEval)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in fetch_all_moves(state, RED, game):
            evaluation = minimax(move, depth-1, alpha, beta, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
            beta = min(beta, minEval)
            if beta <= alpha:
                break
        return minEval, best_move

def simulate_move(piece, move, checker_brd, game, skip):
    checker_brd.move(piece, move[0], move[1])
    if skip:
        checker_brd.remove(skip)

    return checker_brd


def fetch_all_moves(checker_brd, colour, game):
    moves = []

    for checker_pce in checker_brd.fetch_all_chceker_pce(colour):
        valid_moves = checker_brd.fetch_valid_moves(checker_pce)
        for move, skip in valid_moves.items():
            temp_checker_brd = deepcopy(checker_brd)
            temp_piece = temp_checker_brd.fetch_checker_pce(checker_pce.line, checker_pce.col)
            new_checker_brd = simulate_move(temp_piece, move, temp_checker_brd, game, skip)
            moves.append(new_checker_brd)
    
    return moves

