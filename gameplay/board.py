import pygame
from interface.constants import COLOR_LSQ, COLOR_LAST_MOVE_DARK, COLOR_DSQ, SQUARE_SIZE, ROWS, COLS, COLOR_LAST_MOVE
from .piece import Piece
import copy
import numpy as np

class Board:

    background = np.array([[" ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " "],
                           [" ", " ", " ", " ", " "]])

    initial_board = [["b", "b", "B", "b", "b"],
                    [0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0], 
                    ["w", "w", "W", "w", "w"]]

    def __init__(self, win, deck):
        self.win = win
        self.deck = deck

        self._create_board()
        self._update()

    def __repr__(self):
        return self.bn_board

    def _draw_squares(self):
        self.win.fill(COLOR_LSQ)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(self.win, COLOR_DSQ, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def _draw_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw()

    def _make_bn_board(self):
        list_bn = []

        to_find = "W"
        for ii in range(self.wmaterial):
            row, col = np.where(self.array_board == to_find)
            piece = self.get_piece(row, col)
            list_bn.append(piece.short_rc)

            if ii == 0:
                to_find = "w"

        for c in self.deck.wcards:
            list_bn.append(c.short_name)

        to_find = "B"
        for ii in range(self.bmaterial):
            row, col = np.where(self.array_board == to_find)
            piece = self.get_piece(row, col)
            list_bn.append(piece.short_rc)
            
            if ii == 0:
                to_find = "b"

        for c in self.deck.bcards:
            list_bn.append(c.short_name)

        self.bn_board = "".join(list_bn)

    def _make_array_board(self):
        self.array_board = Board.background
        for row in range(ROWS):
            for col in range(COLS): 
                piece = self.board[row][col]
                if piece:
                    self.array_board[row][col] = piece.letter

    def _count_material(self):
        self.wmaterial = 0
        self.bmaterial = 0
        self.list_material = [self.wmaterial, self.bmaterial]

        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece:
                    self.list_material[piece.side] += 1 

    def _update(self):
        self._count_material()
        self._make_array_board()
        self._make_bn_board()
        self._is_win()

    def _is_win(self):
        if not self._is_king_alive(0):
            self.winner = 1
        elif not self._is_king_alive(1):
            self.winner = 0
        elif self.get_piece(0, 2) and self.get_piece(0, 2).side == 0 and self.get_piece(0, 2).king:
            self.winner = 0
        elif self.get_piece(4, 2) and self.get_piece(4, 2).side == 1 and self.get_piece(4, 2).king:
            self.winner = 1
        else: 
            self.winner = None

    def _is_king_alive(self, side):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.get_piece(row, col)
                if piece and piece.side == side and piece.king:
                    return True
        return False

    def _create_board(self):
        self.board = Board.initial_board
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == 0:
                    continue
                elif self.board[row][col] == "b":
                    self.board[row][col] = Piece(row, col, 1, self.win)
                elif self.board[row][col] == "B":
                    self.board[row][col] = Piece(row, col, 1, self.win)
                    self.board[row][col].make_king()
                elif self.board[row][col] == "w":
                    self.board[row][col] = Piece(row, col, 0, self.win)
                elif self.board[row][col] == "W":
                    self.board[row][col] = Piece(row, col, 0, self.win)
                    self.board[row][col].make_king()

    def draw(self):
            self._draw_squares()
            self._draw_pieces()   

    def draw_single_square(self, row, col, last_move = False):
        if last_move:
            color = COLOR_LAST_MOVE
            if  col in list(range(row % 2, ROWS, 2)):
                color = COLOR_LAST_MOVE_DARK
        else:
            color = COLOR_LSQ
            if  col in list(range(row % 2, ROWS, 2)):
                color = COLOR_DSQ
        pygame.draw.rect(self.win, color, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = 0
        self.board[row][col] = piece
        piece.move(row, col)
        self._update()

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_valid_moves(self, piece, card, side):
        valid_moves = []
        for move in card.moves:
            row, col = piece.row + (2*side-1)*move[1], piece.col + (1-2*side)*move[0]
            if row > 4 or col > 4 :
                continue
            elif row < 0 or col < 0 :
                continue
            elif self.board[row][col] and self.board[row][col].side == side:
                continue
            else :
                valid_moves.append((row, col))
        return valid_moves