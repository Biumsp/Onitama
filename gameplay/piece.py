from interface.constants import LOAD_PIECES, PIECES_IMAGES, SQUARE_SIZE, OUTLINECOLOR1, OUTLINECOLOR2, COLORPIECES1, COLORPIECES2, PADDING_KING, PADDING_PAWN, OUTLINE
import pygame

class Piece:

    # Diagonally-Symmetric Pieces 
    ds_pieces = {'00': '44', '01': '43', '02': '42', '03': '41',
           '04': '40', '10': '34', '11': '33', '12': '32',
           '13': '31', '14': '30', '20': '24', '21': '23', 
           '22': '22', '23': '21', '24': '20', '30': '14', 
           '31': '13', '32': '12', '33': '11', '34': '10', 
           '40': '04', '41': '03', '42': '02', '43': '01', 
           '44': '00'}

    # Horizontally-Symmetric Pieces
    hs_pieces = {'00': '40', '01': '41', '02': '42', '03': '43', 
           '04': '44', '10': '30', '11': '31', '12': '32', 
           '13': '33', '14': '34', '20': '20', '21': '21', 
           '22': '22', '23': '23', '24': '24', '30': '10', 
           '31': '11', '32': '12', '33': '13', '34': '14', 
           '40': '00', '41': '01', '42': '02', '43': '03', 
           '44': '04'}

    def __init__(self, row, col, side, win):
        self.row = row
        self.col = col

        self.win = win

        self.side = side
        self.king = False

        if self.side == 0:
            self.color = COLORPIECES1
            self.outline_color = OUTLINECOLOR1
            self.letter = "w"
        else:
            self.color = COLORPIECES2
            self.outline_color = OUTLINECOLOR2
            self.letter = "b"
        
        self.x = 0
        self.y = 0
        self._calc_pos()

        self.hsp = Piece.hs_pieces[self.short_rc]
        self.dsp = Piece.ds_pieces[self.short_rc]

        self._get_image()

    def __repr__(self):
        return "<Piece: c = {}, r = {}, c = {}>".format(["W", "B"][self.side], self.row, self.col)

    def _calc_pos(self):
        self.short_rc = "".join([str(self.row), str(self.col)])

        # Circular pieces are drawn from their centre
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE//2
    
    def _get_image(self):
        if LOAD_PIECES:
            if self.side == 0:
                side_letter = "w"
            else: 
                side_letter = "b"

            if self.king:
                role_letter = "K"
            else:
                role_letter  = "P"

            name = side_letter + role_letter
            self.image = PIECES_IMAGES[name.lower()]

    def move(self, row, col):
        self.row = row
        self.col = col
        self._calc_pos()

    def make_king(self):
        self.king = True
        self.letter = self.letter.upper()
        self._get_image()
        
    def draw(self):
        if LOAD_PIECES:
            x, y = self.x - self.image.get_size()[0]//2, self.y - self.image.get_size()[1]//2
            self.win.blit(self.image, (x, y))
        else:
            if self.king:
                radius = SQUARE_SIZE//2 - PADDING_KING
                pygame.draw.circle(self.win, self.outline_color, (self.x, self.y), radius + OUTLINE)
                pygame.draw.circle(self.win, self.color, (self.x, self.y), radius)
                pygame.draw.circle(self.win, self.outline_color, (self.x, self.y), radius/3)
            else:
                radius = SQUARE_SIZE//2 - PADDING_PAWN
                pygame.draw.circle(self.win, self.outline_color, (self.x, self.y), radius + OUTLINE)
                pygame.draw.circle(self.win, self.color, (self.x, self.y), radius)        