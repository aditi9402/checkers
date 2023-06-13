import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece

class Board:
    def __init__(self):
        self.checker_brd = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_checker_brd()
    
    def draw_squares(self, win): 
        win.fill(BLACK)
        for line in range(ROWS):
            for col in range(line % 2, COLS, 2):
                pygame.draw.rect(win, RED, (line*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    #This line of code is returning the value of the current state of the game in a board game. The function is used to evaluate the state of the game and to estimate which player is in a better position to win the game.
    # The reason for adding half of the difference is to give some advantage to the player who has more kings.
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.6 - self.red_kings * 0.6)

    def fetch_all_chceker_pce(self, colour):
        chceker_pce = []
        for line in self.checker_brd:
            for checker_pce in line:
                if checker_pce != 0 and checker_pce.colour == colour:
                    chceker_pce.append(checker_pce)
        return chceker_pce

    def move(self, checker_pce, line, col):
        self.checker_brd[checker_pce.line][checker_pce.col], self.checker_brd[line][col] = self.checker_brd[line][col], self.checker_brd[checker_pce.line][checker_pce.col]
        checker_pce.move(line, col)

        if line == ROWS - 1 or line == 0:
            checker_pce.make_king()
            if checker_pce.colour == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def fetch_checker_pce(self, line, col):
        return self.checker_brd[line][col]

    def create_checker_brd(self): # checker_pce object
        for line in range(ROWS):
            self.checker_brd.append([])
            for col in range(COLS):
                if col % 2 == ((line +  1) % 2):
                    if line < 3:
                        self.checker_brd[line].append(Piece(line, col, WHITE))
                    elif line > 4:
                        self.checker_brd[line].append(Piece(line, col, RED))
                    else:
                        self.checker_brd[line].append(0)
                else:
                    self.checker_brd[line].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for line in range(ROWS):
            for col in range(COLS):
                checker_pce = self.checker_brd[line][col]
                if checker_pce != 0:
                    checker_pce.draw(win)

    def remove(self, chceker_pce):
        for checker_pce in chceker_pce:
            self.checker_brd[checker_pce.line][checker_pce.col] = 0
            if checker_pce != 0:
                if checker_pce.colour == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def fetch_valid_moves(self, checker_pce):
        moves = {} 
        left = checker_pce.col - 1
        right = checker_pce.col + 1
        line = checker_pce.line

        if checker_pce.colour == RED or checker_pce.king:
            moves.update(self._traverse_left(line -1, max(line-3, -1), -1, checker_pce.colour, left))
            moves.update(self._traverse_right(line -1, max(line-3, -1), -1, checker_pce.colour, right))
        if checker_pce.colour == WHITE or checker_pce.king:
            moves.update(self._traverse_left(line +1, min(line+3, ROWS), 1, checker_pce.colour, left))
            moves.update(self._traverse_right(line +1, min(line+3, ROWS), 1, checker_pce.colour, right))
    
        return moves

    #_traverse_left method is a helper method used by the fetch_valid_moves method in the checker_brd class
    def _traverse_left(self, start, stop, step, colour, left, skipped=None):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.checker_brd[r][left]
            if current == 0: #found empty square
                if skipped and not last: 
                    break
                elif skipped: #last is not empty #skipped keeps track of any checker_pce that was skipped in the past
                    moves[(r, left)] = last + skipped #last checker we jumped + the checker we jumped on this move
                else:
                    moves[(r, left)] = last #if last has a entry, it means we have skipped a checker_pce in two rows
                
                if last:
                    if step == -1:
                        line = max(r-3, 0)
                    else:
                        line = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, line, step, colour, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, line, step, colour, left+1,skipped=last))
                break
            elif current.colour == colour: #cannot jump oer the same colour as us
                break
            else: #if it's another colour can move over it, assuming it's an empty square next
                last = [current] 

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, colour, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.checker_brd[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        line = max(r-3, 0)
                    else:
                        line = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, line, step, colour, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, line, step, colour, right+1,skipped=last))
                break
            elif current.colour == colour:
                break
            else:
                last = [current]

            right += 1
        
        return moves