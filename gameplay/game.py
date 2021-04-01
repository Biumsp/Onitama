import pygame
from onitama.interface.constants import WIDTH_BOARD, HEIGHT_BOARD, COLOR_SELECTED_PIECE, PURPLE,COLOR_VALID_CAPTURE, COLOR_VALID_MOVES, WIDTH, HEIGHT, SQUARE_SIZE, DRAW_VALID_MOVES, SIZE_VALID_MOVES
from onitama.gameplay.board import Board
from onitama.gameplay.deck import Deck
from onitama.evaluation.position import Position
import time

class Game:
    def __init__(self, DEPTH, position):
        WIN = pygame.display.set_mode((WIDTH, HEIGHT))
        self.win = WIN
        self.depth = DEPTH
        self._init(position=position)

    def _update_history(self):
        if self.semimove not in self.history:
            self.history.update({self.semimove : self.board.bn_board})

    def _update_bn(self):
        self.actual_bn = self.history[self.semimove]
        self.board.board_from_bn(self.actual_bn)

    def _init(self, position = 0):
        if position:
            self.position = position
            self.cards = self._to_cards(self.position)
        self.selected_piece = None
        self.selected_card = None
        self.deck = Deck(self.win, self.cards)
        self.board = Board(self.win, self.deck, self.position)
        self.turn = 0
        self.valid_moves = []
        self.sym_game = self.deck.sym_deck
        self.history = {}
        self.semimove = 0
        self.winner = None
        self.last_move = None
        self.update()

    def _move(self, row, col):
        if self.selected_piece and (row, col) in self.valid_moves:
            self.last_move = [self.selected_piece.row, self.selected_piece.col, row, col]
            self.deck.move(self.selected_card)
            self.board.move(self.selected_piece, row, col)
            self._after_move()
            return True
        else:
            return False

    def _after_move(self):
        self.semimove += 1
        self.change_turn()
        self.selected_card = None
        self.selected_piece = None
        self.valid_moves = []
        self.update()
        self._is_win()

    def _engine_play(self):
        if self.turn:
            pos = Position(self.board.bn_board, self.turn^1)
            pos.find_best_move(self.depth)
            best_move = Position(pos.best_move, self.turn)
            self._init(best_move)
            self._is_win()
        else:
            pass

    def _is_win(self):
        if self.board.winner == 0:
            self.winner = "White"
        elif self.board.winner == 1:
            self.winner = "Black"

        if self.winner:
            time.sleep(3)
            self._draw_win()
            pygame.display.update()
            pygame.time.delay(10000)

    def _to_cards(self, position):
        black_cards = position.cards[0]
        white_cards = position.cards[1]
        return [white_cards, black_cards]

    def _draw_win(self):
        y, x = HEIGHT_BOARD//2, WIDTH_BOARD//2
        pygame.draw.circle(self.win, PURPLE, (y, x), 200)

    def _draw_valid_moves(self):
        if DRAW_VALID_MOVES:
            for move in self.valid_moves:
                row, col = move
                x, y = row*SQUARE_SIZE, col*SQUARE_SIZE
                if not self.board.get_piece(row, col):
                    pygame.draw.circle(self.win, COLOR_VALID_MOVES, (y + SQUARE_SIZE//2, x + SQUARE_SIZE//2), SIZE_VALID_MOVES)
                else:
                    self.board.draw_single_square(row, col)
                    self.board.get_piece(row, col).draw()
                    points = [(y, x), (y, x + SQUARE_SIZE//3),
                              (y + SQUARE_SIZE*3//24, x + SQUARE_SIZE*3//24), (y + SQUARE_SIZE//3, x)]
                    pygame.draw.polygon(self.win, COLOR_VALID_CAPTURE, points)
                    points = [(y, x+SQUARE_SIZE), (y, x + SQUARE_SIZE*2//3),
                              (y + SQUARE_SIZE*3//24, x + SQUARE_SIZE*21//24), (y + SQUARE_SIZE//3, x + SQUARE_SIZE)]
                    pygame.draw.polygon(self.win, COLOR_VALID_CAPTURE, points)
                    points = [(y + SQUARE_SIZE, x), (y + SQUARE_SIZE, x + SQUARE_SIZE//3),
                              (y + SQUARE_SIZE*21//24, x + SQUARE_SIZE*3//24), (y + SQUARE_SIZE*2//3, x)]
                    pygame.draw.polygon(self.win, COLOR_VALID_CAPTURE, points)
                    points = [(y + SQUARE_SIZE, x + SQUARE_SIZE), (y + SQUARE_SIZE, x + SQUARE_SIZE*2//3),
                              (y + SQUARE_SIZE*21//24, x + SQUARE_SIZE*21//24), (y + SQUARE_SIZE*2//3, x + SQUARE_SIZE)]
                    pygame.draw.polygon(self.win, COLOR_VALID_CAPTURE, points)

    def _draw_selected_square_and_piece(self):
        if self.selected_piece:
            row, col = self.selected_piece.row, self.selected_piece.col
            pygame.draw.rect(self.win, COLOR_SELECTED_PIECE, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            self.selected_piece.draw()

    def _draw_last_move(self):
        if self.last_move:
            self.board.draw_single_square(self.last_move[1], self.last_move[0], last_move = True)
            if not (self.selected_piece and (self.last_move[2], self.last_move[3]) in self.valid_moves):
                self.board.draw_single_square(self.last_move[3], self.last_move[2], last_move = True)
            self.board.get_piece(self.last_move[2], self.last_move[3]).draw()

    def _draw_stuff(self):
        self.board.draw()
        self._draw_selected_square_and_piece()
        self._draw_last_move()
        self._draw_valid_moves()
        self.deck.draw()

    def update(self):
        self._update_history()
        self._draw_stuff()
        pygame.display.update()

    def reset(self):
        self._init()

    def go_back(self):
        if self.semimove >= 1:
            self.semimove -= 1
            self._update_history()
            self._update_bn()
    
    def go_forward(self):
        if self.semimove < max(list(self.history.keys())):
            self.semimove += 1
            self._update_history()
            self._update_bn()

    def select_piece(self, row, col):
        if self.selected_card:
            if self.selected_piece:
                result = self._move(row, col)
                if not result:
                    self.selected_piece = None
                    self.wrong_selection()
                    self.select_piece(row, col)
            
            piece = self.board.get_piece(row, col)
            if piece != 0 and piece.side == self.turn:
                self.selected_piece = piece
                self.valid_moves = self.board.get_valid_moves(piece, self.selected_card, self.turn)
                return True
            
        return False

    def wrong_selection(self):
        self.valid_moves = []
        self.update()

    def select_card(self, x, y):
        card = self.deck.get_card(x, y, self.turn)
        self.wrong_selection()
        self.selected_card = card

    def change_turn(self):
        self.valid_moves = []
        self.turn = self.turn^1