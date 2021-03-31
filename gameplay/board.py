import pygame
from onitama.interface.constants import COLOR_LSQ, COLOR_LAST_MOVE_DARK, COLOR_DSQ, SQUARE_SIZE, ROWS, COLS, COLOR_LAST_MOVE
from onitama.gameplay.piece import Piece
from onitama.gameplay.deck import Deck
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

    def __init__(self, win, deck, position = 0):
        self.win = win
        self.deck = deck

        self._create_board(position)
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

        for row in range(ROWS):
            for col in range(COLS):
                if self.array_board[row][col] == "B":
                    list_bn.append(str(col)+str(4-row))
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.array_board[row][col] == "b":
                    coordinate = str(col)+str(4-row)
                    if coordinate in list_bn:
                        continue
                    else:
                        list_bn.append(coordinate)

        for c in self.deck.bcards:
            list_bn.append(c.short_name)

        for row in range(ROWS):
            for col in range(COLS):
                if self.array_board[row][col] == "W":
                    list_bn.append(str(col)+str(4-row))
        
        for row in range(ROWS):
            for col in range(COLS):
                if self.array_board[row][col] == "w":
                    coordinate = str(col)+str(4-row)
                    if coordinate in list_bn:
                        continue
                    else:
                        list_bn.append(coordinate)

        for c in self.deck.wcards:
            list_bn.append(c.short_name)

        self.bn_board = "".join(list_bn)

    def _make_array_board(self):
        self.array_board = copy.deepcopy(Board.background)
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

    def _create_board(self, position = 0):
        if position:
            self.board = self._to_board(position)
        else: 
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

    def _to_board(self, position):
        board =  [[0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0], 
                  [0, 0, 0, 0, 0]]

        black_pieces = position.pieces[0]
        white_pieces = position.pieces[1]
        for i in range(len(black_pieces)):
            if i == 0:
                if black_pieces[i] == '99':
                    continue
                else:
                    board[4 - int(black_pieces[i][1])][int(black_pieces[i][0])] = 'B'
            else:
                board[4 - int(black_pieces[i][1])][int(black_pieces[i][0])] = 'b'

        for i in range(len(white_pieces)):
            if i == 0:
                if white_pieces[i] == '99':
                    continue
                else:
                    board[4 - int(white_pieces[i][1])][int(white_pieces[i][0])] = 'W'
            else:
                board[4 - int(white_pieces[i][1])][int(white_pieces[i][0])] = 'w'

        return board


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