from interface.constants import CARDS_IMAGES, WIDTH_CARD, HEIGHT_CARD, HEIGHT, WIDTH_BOARD
import pygame
import copy

class Card:

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

    cards_moves = {
        "a" : ((0, 2), (0, -1)),
        "b" : ((-1, -1), (1, -1), (-2, 1), (2, 1)),
        "c" : ((-1, 1), (-2, 0), (1, -1)),
        "d" : ((-1, -1), (1, 1), (2, 0)),
        "e" : ((-2, 0), (2, 0), (0, 1)),
        "f" : ((-1, 0), (1, 0), (1, 1), (-1, 1)),
        "g" : ((-1, 0), (-1, 1), (1, 0), (1, -1)),
        "h" : ((1, 1), (1, 0), (-1, 0), (-1, -1)),
        "i" : ((-1, -1), (-1, 1), (1, 1), (1, -1)),
        "j" : ((-1, 1), (1, 1), (0, -1)),
        "k" : ((-1, 0), (0, 1), (0, -1)),
        "l" : ((1, 0), (0, 1), (0, -1)),
        "m" : ((0, 1), (1, -1), (-1, -1)),
        "n" : ((0, 1), (-1, 0), (1, 0)),
        "o" : ((-1, 1), (-1, -1), (1, 0)),
        "p" : ((-1, 0), (1, 1), (1, -1))
    }

    symmetric_cards = {"g" : "h", "h" : "g", "c" : "d", "d" : "c",
          "k" : "l", "l" : "k", "o" : "p", "p" : "o"}

    def __init__(self, c, win, side):
        self.short_name = c
        self.win = win
        self.side = side
        self.name = self.cards_names[c]
        self.moves = self.cards_moves[c]

        if c in self.symmetric_cards:
            self.sym_c = self.symmetric_cards[c]
        else:
            self.sym_c = None

        self._get_image()

    def __repr__(self):
        return self.name

    def _get_image(self):
        if self.short_name.lower() in CARDS_IMAGES:
            self.image = CARDS_IMAGES[self.short_name.lower()]
        else:
            self.image = CARDS_IMAGES[self.name.lower()]

    def draw(self, index):
        image = pygame.transform.rotate(self.image, 180*self.side)
        if self.side:
            x = WIDTH_BOARD + index*WIDTH_CARD
            y = 0
        else:
            x = WIDTH_BOARD + index*WIDTH_CARD
            y = HEIGHT-HEIGHT_CARD

        if index == 2:
            image = pygame.transform.scale(self.image, (WIDTH_CARD*2//3, HEIGHT_CARD*2//3))
            if not self.side:
                y = HEIGHT-HEIGHT_CARD*2//3

        self.win.blit(image, (x, y))

    def change_side(self):
        self.side = self.side^1