from onitama.interface.printing import HiddenPrints
with HiddenPrints():
    import pygame
from onitama.interface.constants import WIDTH, HEIGHT, SQUARE_SIZE, WIDTH_BOARD, FPS, WIDTH_CARD
from onitama.gameplay.game import Game
from onitama.evaluation.position import Position
import time
from random import randint
import sys

filler = "-"*100
big_filler = filler + "\n\n" + filler

cards_names = {
        "a" : "Tiger",
        "b" : "Dragon",
        "c" : "Frog",
        "d" : "Rabbit",
        "e" : "Crab",
        "f" : "Elephant",
        "g" : "Goose",
        "h" : "Rooster",
        "i" : "Monkey",
        "j" : "Mantis",
        "k" : "Horse",
        "l" : "Ox",
        "m" : "Crane",
        "n" : "Boar",
        "o" : "Eel",
        "p" : "Cobra"
    }

pygame.init()
pygame.display.set_caption('Onitama')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col

def main(DEPTH, initial_position, engine, ENGINE_SIDE):
    run = True
    clock = pygame.time.Clock()
    game = Game(DEPTH, initial_position)

    while run:
        clock.tick(FPS)

        if engine:
            if game.turn == ENGINE_SIDE:
                t0 = time.process_time()
                game.engine_play()
                t1 = time.process_time()
                print('\nEnlapsed in {:.2f} [s]'.format(t1 - t0))

                pygame.event.get()
                game.update()
                continue

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


def get_user_inputs():
    DEPTH = 0
    if len(sys.argv) == 2:
        path = sys.argv[1]
        with open(path, 'r') as file:
            initial_position = file.read()
    else:
        condition = True
        while condition:
            random = input("\nRandom game? (y/n)\n")

            if random == 'y':
                initial_position = get_initial_position(random = True)
                condition = False

            elif random == 'n':
                initial_position = get_initial_position()
                condition = False
    
    initial_position = Position(initial_position, 1)   
    turn = int(len(initial_position.cards[1]) > len(initial_position.cards[0]))
    initial_position = Position(initial_position.pos, turn)

    engine, ENGINE_SIDE = get_game_info()
    if engine:
        condition = True
        while condition:
            try :                
                DEPTH = int(input('\nSelect the opponent strength: input a number between 1 and 10\n'))
                condition = False
            except:
                pass
            
    return DEPTH, initial_position, engine, ENGINE_SIDE


def get_game_info():
    condition = True
    while condition :
        info_engine = input("\nDo you want to play against the engine? (y/n)\n")

        if info_engine == 'y':
            engine = 1
            condition = False
        
        elif info_engine == 'n':
            engine = 0
            condition = False
    
    condition = True
    ENGINE_SIDE = 1
    if engine:
        while condition :
            info_engine = input("\nDo you want to play white? (y/n)\n")

            if info_engine == 'y':
                ENGINE_SIDE = 1
                condition = False
            
            elif info_engine == 'n':
                ENGINE_SIDE = 0
                condition = False

    return engine, ENGINE_SIDE


def random_cards(b, w):

    cards = list(cards_names.keys())
    bcards = []
    wcards = []
    for jj in range(5):
        ii = randint(0, 15-jj)
        if jj < 2:
            bcards.append(cards[ii])
        else:
            wcards.append(cards[ii])
        cards.pop(ii)

    return bcards, wcards

def get_initial_position(random = False):

    if random:
        black_cards, white_cards = random_cards(2, 3)
        return "24041434442" + "".join(black_cards) +  "2000103040" + "".join(white_cards)

    # Keep asking for the cards untill the input is acceptable
    condition = True
    while condition :

        # Display the cards' labels and names
        print("\n")
        print(filler)
        print("Cards\t\tLabels")
        print(filler, "\n")

        for label, name in cards_names.items():

            # If the length of the name is >= 8, print only one tab
            print("{}\t{}{}".format(name, "\t"*int(len(name) < 8), label))

        print("\n")
        print(big_filler)

        # Get the cards from user
        input_cards = input("\nSelect the cards: ").split()

        if len(input_cards) == 5 and len(set(input_cards)) == 5:
            condition = False

            for c in input_cards :
                if c not in list(cards_names.keys()) :
                    print("\nInvalid input: select 5 different cards from the list and write them like this 'a b c d e'")
                    condition = True
                    break

            black_cards = input_cards[0:2]
            white_cards = input_cards[2:5]
            initial_position = "24041434442" + "".join(black_cards) +  "2000103040" + "".join(white_cards)

        else:
            print("\nInvalid input: select 5 different cards from the list and write them like this 'a b c d e'")
    return initial_position

if __name__ == '__main__':
    
    DEPTH, initial_position, engine, ENGINE_SIDE = get_user_inputs()
    main(DEPTH, initial_position, engine, ENGINE_SIDE)