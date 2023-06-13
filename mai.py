import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE, BLACK
from checkers.game import Game 
from algorith import minimax
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.init() 
pygame.font.init()

FONT = pygame.font.SysFont("comicsansms", 72)

FPS = 60
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
game = Game(screen)

is_running = True
clock = pygame.time.Clock() #get

def fetch_line_col_from_mouse(pos):
    x, y = pos
    line = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return line, col


screen.fill(BLACK)
font = pygame.font.Font(None, 36)
playHandle = pygame.Rect(180, 150, 200, 100)
exitHandle = pygame.Rect(180, 300, 200, 100)
singleHandle = pygame.Rect(180, 150, 200, 100)
twoHandle = pygame.Rect(180, 300, 200, 100)
easyHandle = pygame.Rect(180, 150, 200, 100)
mediumHandle = pygame.Rect(180, 300, 200, 100)
hardHandle = pygame.Rect(180, 450, 200, 100)

def show_message(message):
    run = True
    while run:
        pygame.init()
        # create text surface for displaying messages
        text = FONT.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))
        WIN.blit(text, text_rect)
        pygame.display.update()
        pygame.time.wait(2000) # wait 2 seconds before continuing

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


def game_ai(depth):
    is_running_game = True
    while is_running_game:
        clock.tick(FPS)

        if game.turn == WHITE:
            pygame.time.wait(500)
            value, new_checker_brd = minimax(game.fetch_checker_brd(), depth, float('-inf'), float('inf'), RED, game)
            game.ai_move(new_checker_brd)

        if game.winner() != None:
            if game.winner() == RED:
                show_message("YOU WIN")
            else:
                show_message("YOU LOSE")
            is_running_game = False    

        if game.turn==WHITE:
            best_valid_moves={}
            for piece in game.checker_brd.fetch_all_chceker_pce(WHITE):
                valid_moves=game.checker_brd.fetch_valid_moves(piece)
                if valid_moves !={}:
                    best_valid_moves=valid_moves
            if best_valid_moves=={}:
                    show_message("YOU WIN") 
                    is_running_game = False 

        if game.turn==RED: 
            best_valid_moves={}
            for piece in game.checker_brd.fetch_all_chceker_pce(RED):
                valid_moves=game.checker_brd.fetch_valid_moves(piece)
                if valid_moves !={}:
                    best_valid_moves=valid_moves
            if best_valid_moves=={}:
                    show_message("AI WINS")
                    is_running_game = False                         

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                line, col = fetch_line_col_from_mouse(pos)
                game.select(line, col)

        game.update()

    pygame.quit()

def game_two():
    is_running_game = True
    clock = pygame.time.Clock()
    game = Game(screen)

    while is_running_game:
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            is_running_game = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running_game = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                line, col = fetch_line_col_from_mouse(pos)
                game.select(line, col)

        game.update()

    pygame.quit()


while is_running:
    clock.tick(FPS)

    pygame.draw.rect(screen, RED, playHandle, border_radius=50)
    text = font.render("Play Game", True, (0, 0, 0))
    text_rect = text.get_rect(center=playHandle.center)
    screen.blit(text, text_rect)

    pygame.draw.rect(screen, WHITE, exitHandle, border_radius=50)
    text = font.render("Exit Game", True, (0, 0, 0))
    text_rect = text.get_rect(center=exitHandle.center)
    screen.blit(text, text_rect)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if playHandle.collidepoint(pos):
                while is_running:

                    pygame.draw.rect(screen, RED, singleHandle, border_radius=50)
                    text = font.render("Single Player", True, (0, 0, 0))
                    text_rect = text.get_rect(center=singleHandle.center)
                    screen.blit(text, text_rect)

                    pygame.draw.rect(screen, WHITE, twoHandle, border_radius=50)
                    text = font.render("Two Player", True, (0, 0, 0))
                    text_rect = text.get_rect(center=twoHandle.center)
                    screen.blit(text, text_rect)
                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            is_running = False

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pos = pygame.mouse.get_pos()
                            if singleHandle.collidepoint(pos):
                                screen.fill(BLACK)
                                while is_running:

                                    pygame.draw.rect(screen, RED, easyHandle, border_radius=50)
                                    text = font.render("Easy Mode", True, (0, 0, 0))
                                    text_rect = text.get_rect(center=easyHandle.center)
                                    screen.blit(text, text_rect)

                                    pygame.draw.rect(screen, RED, mediumHandle, border_radius=50)
                                    text = font.render("Medium Mode", True, (0, 0, 0))
                                    text_rect = text.get_rect(center=mediumHandle.center)
                                    screen.blit(text, text_rect)
                                    pygame.display.update()

                                    pygame.draw.rect(screen, RED, hardHandle, border_radius=50)
                                    text = font.render("Hard Mode", True, (0, 0, 0))
                                    text_rect = text.get_rect(center=hardHandle.center)
                                    screen.blit(text, text_rect)
                                    pygame.display.update()

                                    for event in pygame.event.get():
                                        if event.type == pygame.QUIT:
                                            is_running = False

                                        if event.type == pygame.MOUSEBUTTONDOWN:
                                            pos = pygame.mouse.get_pos()

                                            if easyHandle.collidepoint(pos):
                                                game_ai(1)
                                            elif mediumHandle.collidepoint(pos):
                                                game_ai(2)
                                            elif hardHandle.collidepoint(pos):
                                                game_ai(4)

                            elif twoHandle.collidepoint(pos):
                                game_two()

            elif exitHandle.collidepoint(pos):
                is_running = False

pygame.quit()