import pygame

WIDTH, HEIGHT = 600, 600
ROWS, COLS= 8, 8
SQUARE_SIZE = WIDTH//COLS

# rgb value
RED = (245, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 245)
GREY = (128,128,128)

CROWN = pygame.transform.scale(pygame.image.load('D:\iiitg\sem4\AI\Python-Checkers-AI-master\Python-Checkers-AI-master\crown.png'), (44, 25))
