import pygame
from onitama.interface.constants import WIDTH, HEIGHT, SQUARE_SIZE, WIDTH_BOARD, FPS, WIDTH_CARD
from onitama.gameplay.game import Game
import time
import sys

pygame.init()
pygame.display.set_caption('Onitama')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                game.update()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > WIDTH_BOARD and pos[0] < (WIDTH_BOARD + 3*WIDTH_CARD):
                    game.select_card(pos[0], pos[1])
                else:
                    row, col = get_row_col_from_mouse(pos)
                    game.select_piece(row, col)
                    game.update()
            
            #elif event.type == pygame.KEYDOWN:
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                game.go_back()
                game.update()

            elif pressed[pygame.K_RIGHT]:
                game.go_forward()
                game.update()

        if game.winner:
            run = False            

    pygame.quit()


if __name__ == '__main__':
    main()