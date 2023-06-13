import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from checkers.board import Board 

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
    
    def update(self):
        self.checker_brd.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self): 
        self.selected = None
        self.checker_brd = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self):
        return self.checker_brd.winner()

    def reset(self):
        self._init()

    def select(self, line, col):
        if self.selected: #if selected
            result = self._move(line, col) #try to move it to line, col
            if not result: #if not possible
                self.selected = None #clear current selection
                self.select(line, col) #reselect something else(call this method again)
        
        checker_pce = self.checker_brd.fetch_checker_pce(line, col)
        if checker_pce != 0 and checker_pce.colour == self.turn:
            self.selected = checker_pce
            self.valid_moves = self.checker_brd.fetch_valid_moves(checker_pce)
            return True
            
        return False

    def _move(self, line, col): 
        checker_pce = self.checker_brd.fetch_checker_pce(line, col)
        if self.selected and checker_pce == 0 and (line, col) in self.valid_moves:
            self.checker_brd.move(self.selected, line, col)
            skipped = self.valid_moves[(line, col)]
            if skipped:
                self.checker_brd.remove(skipped)
            self.change_turn()  
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            line, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, line * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def fetch_checker_brd(self):
        return self.checker_brd

    def ai_move(self, checker_brd):
        self.checker_brd = checker_brd
        self.change_turn()