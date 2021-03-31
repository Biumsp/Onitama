import re
import copy
from onitama.main import get_row_col_from_mouse, main
from onitama.evaluation.evaluation import evaluate_pos

class Position():

    cards = {
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

    def __init__(self, pos, turn, current_tree = {}, WIN = 0):
        self.pos = pos
        self.turn = turn
        self.WIN = WIN

        self.pieces = []
        self.cards  = []
        self.divide()

        self.next_pos = False
        self.current_tree = current_tree
        self.best_move = None
        self.value = 0
        self.evaluated = False
        self.ordered_next_pos = False

        self.is_win = False
        self._is_win()

        self.protection_mark = 0

        self._display()
        
    def __str__(self):
        return self.pos

    
    def _display(self):
        if self.WIN:
            main(self, 1000, self.WIN)


    def _get_next_pos(self):
        """ Creates a list of legal next pos"""
        
        # =========================================================
        # Get the list of possible positions

        self.next_pos = []        
        next_pos_str = []

        for card in self.cards[self.turn][0:-1]:
            for move in Position.cards[card]:
                for piece in self.pieces[self.turn]:

                    # Get actual piece position and modify it
                    piece_position = [int(j) for j in piece]
                    next_piece_position = [piece_position[0] + (2*self.turn - 1)*move[0], piece_position[1] + (2*self.turn - 1)*move[1]]

                    # Discard the move if out of boundaries
                    if next_piece_position[0] > 4 or next_piece_position[1] > 4 :
                        continue
                    elif next_piece_position[0] < 0 or next_piece_position[1] < 0 :
                        continue

                    # Discard the move if there's a piece of the same side that sqare 
                    elif (str(next_piece_position[0]) + str(next_piece_position[1])) in self.pieces[self.turn]:
                        # Also add 1 to the protection-mark 
                        self.protection_mark += 1
                        continue

                    else :
                        next_piece_position = (str(next_piece_position[0]) + str(next_piece_position[1])) 
                        next_pos_str.append(self.rearrange(piece, next_piece_position, card))

        # =========================================================
        # Check if they are already in the current tree, otherwise add them

        for pos_str in next_pos_str:
            if pos_str in self.current_tree:
                self.next_pos.append(self.current_tree[pos_str])
            else:
                p = Position(pos_str, self.turn^1, self.current_tree, self.WIN)
                self.next_pos.append(p)
                self.current_tree.update({pos_str : p})


    def _order_next_pos(self):
        for p in self.next_pos:
            p._static_evaluation()
        self.next_pos.sort(key = lambda p: p.value, reverse = self.turn)
        self.ordered_next_pos = True


    def _static_evaluation(self):
        """Performs the static evaluation of the position"""
        if not self.evaluated:
            self.value = evaluate_pos(self)
            self.evaluated = True


    def _is_win(self):
        if self.pieces[self.turn][0] == ("2" + str(self.turn*4)):
            mark = (2*self.turn - 1)*float("inf")
        elif self.pieces[self.turn^1][0] == ("2" + str((self.turn^1)*4)):
            mark = -(2*self.turn - 1)*float("inf")
        elif '99' in self.pieces[0]:
            mark = float('inf')
        elif '99' in self.pieces[1]:
            mark = float('-inf')
        else:
            return
        self.value = mark
        self.is_win = True
        self.evaluated = True

    
    def evaluate(self, depth, alpha = float('-inf'), beta = float('inf')):
        """Recursive evaluation using minmax with pruning"""

        if depth == 0 or self.is_win:
            self._static_evaluation()
            return self.value

        if not self.next_pos:
            self._get_next_pos()

        # ======================================================================
        # Hyperparameter Alert: depth from which to order the positions
        # ======================================================================
        if depth <= 5:
            if not self.ordered_next_pos:
                self._order_next_pos()

        if self.turn:
            maxEval = float('-inf')
            for p in self.next_pos:
                eval = p.evaluate(depth - 1, alpha, beta)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.value = maxEval
            self.evaluated = True
            return maxEval

        else:
            minEval = float('inf')
            for p in self.next_pos:
                eval = p.evaluate(depth - 1, alpha, beta)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.value = minEval
            self.evaluated = True
            return minEval


    def divide(self):
        """Divides a position-string in lists of cards and pieces"""

        # Using REGEX to group the position-string in substrings
        r = re.compile(r'(\d+)(\D+)(\d+)(\D+)')
        pieces_0, cards_0, pieces_1, cards_1 = r.match(self.pos).group(1,2,3,4)

        # Creating the correct lists from the substrings
        pieces_0 = re.findall('..',pieces_0)
        pieces_1 = re.findall('..',pieces_1)
        cards_0 = list(cards_0)
        cards_1 = list(cards_1)

        self.pieces = [pieces_0, pieces_1]
        self.cards  = [cards_0, cards_1]


    def rearrange(self, old_piece_pos, new_piece_pos, card):
        """Rearrange the parts of the position-string"""

        # Create internal variables
        pieces_i = copy.deepcopy(self.pieces)
        cards_i = copy.deepcopy(self.cards)

        pieces_i[self.turn].remove(old_piece_pos)

        # Checks if the moving piece is the king
        if old_piece_pos == self.pieces[self.turn][0]:
            pieces_i[self.turn].sort(key = lambda x: int(x))
            pieces_i[self.turn].insert(0, new_piece_pos)

        else:
            pieces_i[self.turn].append(new_piece_pos)
            king_pos = pieces_i[self.turn][0]
            pieces_i[self.turn].remove(king_pos)
            pieces_i[self.turn].sort(key = lambda x: int(x))
            pieces_i[self.turn].insert(0, king_pos)

        if new_piece_pos == pieces_i[self.turn^1][0]:
            # If the opposite king was captured set his value to 99
            pieces_i[self.turn^1][0] = '99'

        else:
            if new_piece_pos in pieces_i[self.turn^1]:
                pieces_i[self.turn^1].remove(new_piece_pos)

        # Now take the used card and give it to the other side
        cards_i[self.turn].remove(card)
        cards_i[self.turn^1].append(card)

        return "".join(pieces_i[0] + cards_i[0] + pieces_i[1] + cards_i[1])


    def find_best_move(self, depth):
        self.evaluate(depth)
        self._order_next_pos()
        self.best_move = self.next_pos[0].pos
        return self.best_move