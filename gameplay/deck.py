from onitama.gameplay.card import Card
import pygame
from onitama.interface.constants import WIDTH_CARD, HEIGHT_CARD, HEIGHT, WIDTH_BOARD, COLOR_BACKGROUND_DECK, WIDTH, HEIGHT

class Deck:
    def __init__(self, win, cards):
        self.win = win
        self.wcards = [Card(c, self.win, 0) for c in cards[0]]
        self.bcards = [Card(c, self.win, 1) for c in cards[1]]
        self.all_cards = self.wcards + self.bcards

        self.sym_deck = self._is_sym_deck()

    def __repr__(self):
        return "<W: {}, B: {}>".format(", ".join([i.name for i in self.wcards]),
                                       ", ".join([i.name for i in self.bcards]))

    def _is_sym_deck(self):
        for c in self.all_cards:
            if not c.sym_c:
                return False
        return True
    
    def _draw_background(self):
        pygame.draw.rect(self.win, COLOR_BACKGROUND_DECK, (WIDTH_BOARD, 0, (WIDTH-WIDTH_BOARD), HEIGHT))

    def _draw_cards(self):
        for c, ii in zip(self.bcards, range(len(self.bcards))):
            c.draw(ii)
        for c, ii in zip(self.wcards, range(len(self.wcards))):                
            c.draw(ii)
            
    def move(self, card):
        if card in self.wcards:
            self.wcards.remove(card)
            self.bcards.append(card)
        else:
            self.bcards.remove(card)
            self.wcards.append(card)

        card.change_side()

    def get_card(self, x, y, side):
        if side:
            if y < HEIGHT_CARD:
                if x  < (WIDTH_BOARD + WIDTH_CARD):
                    return self.bcards[0]
                elif x  < (WIDTH_BOARD + 2*WIDTH_CARD):
                    return self.bcards[1]
        else: 
            if y > (HEIGHT - HEIGHT_CARD):
                if x  < (WIDTH_BOARD + WIDTH_CARD):
                    return self.wcards[0]
                elif x  < (WIDTH_BOARD + 2*WIDTH_CARD):
                    return self.wcards[1]

        return None

    def draw(self):
        self._draw_background()
        self._draw_cards()