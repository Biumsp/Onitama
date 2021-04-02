import pygame
import os
from .themes import *

pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ----------------------------------------------------------------------------
# Settings
# ----------------------------------------------------------------------------

# Display Settings
WIDTH_BOARD, HEIGHT_BOARD = 800, 800
LOAD_PIECES = False
DRAW_VALID_MOVES = True

# Theme Settings
THEME_BOARD = THEMEB_LICHESS
THEME_PIECES = THEMEP_STD
COLOR_BACKGROUND_DECK = GREY

# ----------------------------------------------------------------------------
# Parameters and Variables
# ----------------------------------------------------------------------------

# Frames Per Second
FPS = 60

# Sizes
ROWS, COLS = 5, 5
SQUARE_SIZE = HEIGHT_BOARD//COLS
RESIZE_RATIO = SQUARE_SIZE//160

WIDTH_CARD, HEIGHT_CARD = 225*RESIZE_RATIO, 300*RESIZE_RATIO
WIDTH, HEIGHT = WIDTH_BOARD + 2*WIDTH_CARD + WIDTH_CARD*2//3, HEIGHT_BOARD
PIECE_SIZE = 125*RESIZE_RATIO

PADDING_KING = 20*RESIZE_RATIO
PADDING_PAWN = 40*RESIZE_RATIO
OUTLINE = 2

SIZE_VALID_MOVES = 15*RESIZE_RATIO

# Colors
COLOR_LSQ, COLOR_DSQ, COLOR_VALID_MOVES, COLOR_VALID_CAPTURE, COLOR_SELECTED_PIECE, COLOR_LAST_MOVE, COLOR_LAST_MOVE_DARK = THEME_BOARD
COLORPIECES1, COLORPIECES2, OUTLINECOLOR1, OUTLINECOLOR2 = THEME_PIECES

# Images
CARDS_IMAGES_DIR = os.path.join(BASE_DIR, r'images\cards')
PIECES_IMAGES_DIR = os.path.join(BASE_DIR, r'images\pieces')

CARDS_IMAGES = {}
for name in os.listdir(CARDS_IMAGES_DIR):
    PathImage = os.path.join(CARDS_IMAGES_DIR, name)
    name = os.path.splitext(name)[0].lower()
    image = pygame.transform.scale(pygame.image.load(PathImage), (WIDTH_CARD, HEIGHT_CARD))
    CARDS_IMAGES.update({name : image}) 

PIECES_IMAGES = {}
if LOAD_PIECES:
    for name in os.listdir(PIECES_IMAGES_DIR):
        PathImage = os.path.join(PIECES_IMAGES_DIR, name)
        name = os.path.splitext(name)[0].lower()
        image = pygame.image.load(PathImage)
        image = pygame.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))
        PIECES_IMAGES.update({name : image}) 