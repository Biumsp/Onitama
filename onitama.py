# Onitama-playing software

# ----------------------------------------------------------------------------------------------------------------------
# Import Stuff
# ----------------------------------------------------------------------------------------------------------------------

import os
import re
import sys
import copy
import time
import numpy 
import pickle
import random

# ----------------------------------------------------------------------------------------------------------------------
# Important Variables
# ----------------------------------------------------------------------------------------------------------------------

# Load the dictionary of positions
try:
    if os.path.getsize(r"C:\Desktop\dict_onitama.pkl") > 0:      
        with open(r"C:\Desktop\dict_onitama.pkl", "rb") as file:
            unpickler = pickle.Unpickler(file)
            positions_values = unpickler.load()

    else:
        positions_values = {}

except FileNotFoundError:

    print("Storage file for evaluated moves not found: creating it on desktop")
    positions_values = {}
    with open(r"C:\Desktop\dict_onitama.pkl", "wb") as file:
            pickle.dump(positions_values, file)

filler = "-"*100
big_filler = filler + "\n\n" + filler

# Dictionary of cards' moves
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

# Dicttionary of cards' names
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

# Dictionary of symmetric cards
symmetric_cards = {"g" : "h", "h" : "g", "c" : "d", "d" : "c", "k" : "l", "l" : "k", "o" : "p", "p" : "o"}

# Dictionary of symmetric positions
p = [str(x)+str(y) for x in range(5) for y in range(5)]
dsp = [str(abs(4-x))+str(abs(4-y)) for x in range(5) for y in range(5)]
hsp = [str(abs(4-x))+str(y) for x in range(5) for y in range(5)]
diagonally_symmetric_pieces = dict(zip(p, dsp))
horizontally_symmetric_pieces = dict(zip(p, hsp))

# ----------------------------------------------------------------------------------------------------------------------
# Classes and Functions
# ----------------------------------------------------------------------------------------------------------------------

def divide(pos, only_cards = False, only_pieces = False):
    """Divides a position-string in lists of cards and pieces"""

    # Using REGEX to group the position-string in substrings
    r = re.compile(r'(\d+)(\D+)(\d+)(\D+)')
    pieces_0, cards_0, pieces_1, cards_1 = r.match(pos).group(1,2,3,4)

    # Creating the correct lists from the substrings
    pieces_0 = re.findall('..',pieces_0)
    pieces_1 = re.findall('..',pieces_1)
    cards_0 = list(cards_0)
    cards_1 = list(cards_1)

    # return what was requested
    if only_cards :
        return cards_0 + cards_1
    elif only_pieces :
        return [pieces_0, pieces_1]
    else:
        return pieces_0, cards_0, pieces_1, cards_1

        
def diagonal_symmetry(pos):
    """Creates the diagonally-symmetric position (for every game)"""

    # Divide the position string
    pieces_0, cards_0, pieces_1, cards_1 = divide(pos)

    # Get the symmetric lists
    new_pieces_0 = [diagonally_symmetric_pieces[i] for i in pieces_1]
    new_pieces_1 = [diagonally_symmetric_pieces[i] for i in pieces_0]

    return "".join(new_pieces_0 + cards_1 + new_pieces_1 + cards_0)


def horizontal_symmetry(pos):
    """Creates the horizontally-symmetric position (only for symmetric games)"""

    # Divide the position string
    pieces_0, cards_0, pieces_1, cards_1 = divide(pos)

    # Get the symmetric lists
    new_cards_0 = [symmetric_cards[i] if i in symmetric_cards else i for i in cards_0]
    new_cards_1 = [symmetric_cards[i] if i in symmetric_cards else i for i in cards_1]
    new_pieces_0 = [horizontally_symmetric_pieces[i] for i in pieces_0]
    new_pieces_1 = [horizontally_symmetric_pieces[i] for i in pieces_1]

    # Remember that for every horizontally-symmetric position there's also a diagonally-symmetric one
    return "".join(new_pieces_0 + new_cards_0 + new_pieces_1 + new_cards_1)


def rearrange(pos, piece, next_piece_position, card, pieces, cards):
    """Rearrange the parts of the position-string"""

    # Create internal variables
    pieces_i = copy.deepcopy(pieces)
    cards_i = copy.deepcopy(cards)

    # Let's see who has to move
    i = int((len(cards_i[0]) < len(cards_i[1])))

    # Checks if the moving piece is the king (it has to be done before you modify the list)
    is_king = (piece == pieces_i[i][0])

    # Remove the old piece-position from the list
    pieces_i[i].remove(piece)

    # Add the new piece-position
    pieces_i[i].append(next_piece_position)

    # Save the king position
    if is_king:
        king_position = next_piece_position
    else :
        king_position = pieces_i[i][0]

    # Sort the pieces' positions 
    pieces_i[i].sort(key = lambda x: int(x)) 

    # Now remove the king from wherever he got..
    pieces_i[i].remove(king_position)

    # And put him in front 
    pieces_i[i] = [king_position] + pieces_i[i]

    # If there was a capture remove the piece from the board
    for p in pieces_i[i]:
        try :
            pieces_i[i^1].remove(p)
        except ValueError:
            pass

    # Now take the used card and give it to the other side
    cards_i[i].remove(card)
    cards_i[i^1].append(card)

    return "".join(pieces_i[0] + cards_i[0] + pieces_i[1] + cards_i[1])


def next_positions(pos, cards_moves = cards, false_side = False, protection = False):
    """Computes the string of all possible positions arising from the current one"""

    # Divide the position string
    pieces_0, cards_0, pieces_1, cards_1 = divide(pos)
    pieces_i = [pieces_0, pieces_1]
    cards_i = [cards_0, cards_1]

    # Let's see who has to move
    i = int(len(cards_i[0]) < len(cards_i[1]))

    # Initiate the variable for protection
    mark_protection = 0

    # If you need to false the game and let the second player play..
    if false_side:

        # Invert the boolean value of i
        i = i^1

        # Take the last card from the playing side and add it to those of the falsely playing side
        cards_i[i] += cards_i[i^1][-1]

        # Remove that card from those of the playing side
        cards_i[i^1].pop(-1)

    pieces = pieces_i[i]
    cards = cards_i[i]

    # List of possible positions
    next_pos = []

    for card in cards[0:-1]:
        for move in cards_moves[card]:
            for piece in pieces:

                # Get actual piece position and modify it
                piece_position = [int(j) for j in piece]
                next_piece_position = [piece_position[0] + (1-2*i)*move[0], piece_position[1] + (1-2*i)*move[1]]

                # Discard the move if out of boundaries
                if next_piece_position[0] > 4 or next_piece_position[1] > 4 :

                    # Skip this move
                    continue

                # Discard the move if out of boundaries
                elif next_piece_position[0] < 0 or next_piece_position[1] < 0 :

                    # Skip this move
                    continue

                # Discard the move if there's a piece of the same side that sqare 
                elif (str(next_piece_position[0]) + str(next_piece_position[1])) in pieces:

                    # Also add 1 to the protection-mark 
                    mark_protection += 1

                    # Skip this move
                    continue

                # Otherwise append it to the list
                else :

                    # If you only need protection, skip this move
                    if protection:
                        continue

                    # Make the list-position into a string
                    next_piece_position = (str(next_piece_position[0]) + str(next_piece_position[1])) 

                    # Rearrange the new position and append it to the next_pos list
                    next_pos.append(rearrange(pos, piece, next_piece_position, card, pieces_i, cards_i))
        
    # If you only need protection, return the protection-mark
    if protection:
        return mark_protection

    return list(set(next_pos))


def will_win(pos, side, old_pieces, other_side = False, false_side = False):
    """If it's a win for the specified side returns True"""

    # For all possible positions, get the list of new_pieces
    for position in next_positions(pos, false_side = false_side):

        # Get the new pieces
        new_pieces = divide(position, only_pieces= True)

        # Have you reached the winning square?
        if new_pieces[side][0] == ("2" + str(4 - 4*side)):

            # Make the 1 a -1 and let the 0 be a 0
            mark = (1 - 2*side)*float('inf')

            # Update the database
            update_dict(position, mark)

            return True

        # If the side to play is the right one
        if not other_side:

            # Did the other side lose their king?
            if (old_pieces[side^1][0] != new_pieces[side^1][0]):

                # Make the 1 a -1 and let the 0 be a 0
                mark = (1 - 2*side)*float('inf')

                # Update the database
                update_dict(position, mark)

                return True

    # If the side is not the one who should play
    if other_side:

        # Let the correct side play
        for p in next_positions(pos):

            # Get the pieces in this position
            old_pieces = divide(p, only_pieces=True)

            # And now let the second player play
            for pp in next_positions(p):

                # Get the pieces
                new_pieces = divide(pp, only_pieces=True)

                # If the first side didn't lose their king return False
                if (old_pieces[side^1][0] == new_pieces[side^1][0]):
                    return False
        
        # If in any possible variation the first side loses their king, return True
        return True


def protection(pos, side, pieces_i):
    """Evaluates how protected each side's pawns are"""

    # SHOULD GIVE MORE WEIGHT TO PROTECTED PAWNS THAT ARE ALSO ATTACKED 
    # Sinzìce is better to have protected those

    # Initiate variable
    mark_protection = 0

    # Get protection-mark for the playing side and add it
    mark_protection += next_positions(pos, protection = True)/len(pieces_i[side])

    # Get protection-mark for the other side and subtract it
    mark_protection -= next_positions(pos, false_side = True, protection = True)/len(pieces_i[side^1])

    # Make the 1 a -1 and let the 0 be a 0
    return mark_protection/4


def centrality(pos, pieces_0, pieces_1):
    """Evaluates how central the pieces of each side are"""
    
    # Initiate variables
    centrality_mark_0, centrality_mark_1 = 0, 0

    # Give a mark to every piece
    for piece in pieces_0:

        # The more central the piece, the higher the mark
        centrality_mark_0 += (2 - abs(2 - int(piece[0])))*(2 - abs(2 - int(piece[1])))

    # Give a mark to every piece
    for piece in pieces_1:

        # The more central the piece, the higher the mark
        centrality_mark_1 += (2 - abs(2 - int(piece[0])))*(2 - abs(2 - int(piece[1])))

    # Normalize by the number of pieces of each side (we want an intensive parameter)
    centrality_mark_0 *= 1/len(pieces_0)
    centrality_mark_1 *= 1/len(pieces_1)
    
    # Divide by 4 for normalization
    return centrality_mark_0/4, centrality_mark_1/4


def domination(pos, pieces_0, pieces_1):
    """Evaluates how each side restrictes the other"""
    
    # Initiate variables
    mark_domination_0, mark_domination_1 = 0, 0
    
    # Give a point for every piece y-position
    for piece in pieces_0:

        # But give it only if the opposite king is restricted 
        if int(piece[1]) <= int(pieces_1[0][1]):
            mark_domination_0 += int(piece[1])

    # Give a point for every piece y-position
    for piece in pieces_1:

        # But give it only if the opposite king is restricted 
        if int(piece[1]) >= int(pieces_0[0][1]):
            mark_domination_1 += (4- int(piece[1]))

    # Normalize by the maximum you can get
    return mark_domination_0/15, mark_domination_1/15


def control(pos, side):
    """Number of squares controlled"""

    mark_control = [0, 0]
    # Number of possible moves for the playing side
    mark_control[side] = len(next_positions(pos))/20

    # Number of possible moves for the other side
    mark_control[side^1] = len(next_positions(pos, false_side=True))/20

    return mark_control


def privilege(pos, cards_i):
    """Evaluates the presence of cards with a distinctive move"""
    
    # Initiate variables
    mark_privilege_0, mark_privilege_1 = [], []

    # Create a useful list
    all_cards = cards_i[0] + cards_i[1]
    
    # Get all different possible moves, with repetitions
    all_moves = [m for c in all_cards for m in cards[c]]

    # Get all different moves
    different_moves = list(set(all_moves))

    # Define a dictionary of all different moves
    dict_moves = {}

    # Count occurencies, normalize them and update the dictionary
    for m in different_moves:
        dict_moves.update({m : (len(all_cards) - all_moves.count(m))/len(all_cards)})
  
    # Give a value to each card 
    marks_cards = {}

    # For all cards
    for c in all_cards:

        # Set the partial mark to zero
        partial_mark = 0

        # For every move of that card
        for m in cards[c]:

            # Add the position of that move in the different_moves list to the partial mark
            partial_mark += (dict_moves[m])

        # Then update the overall mark of that card in the dictionary
        marks_cards.update({c : partial_mark})

    # Get the maximum mark that was given to a card
    maximum_mark = max([marks_cards[i] for i in all_cards])

    # Sort all cards by their overall mark
    all_cards.sort(key = lambda x: marks_cards[x], reverse = True)

    # Just a useful list
    marks_privilege = [mark_privilege_0, mark_privilege_1]

    # For all cards
    for c in all_cards:

        # Check if that card is in cards_0 or cards_1
        for i in [0, 1]:
            if c in cards_i[i]:

                # Add the normalized position of the card in the all_card list to the correct mark-variable
                marks_privilege[i].append(marks_cards[c]/maximum_mark)

    # Get the maximum mark that was given to a side
    maximum_mark = max([sum(m) for m in marks_privilege])

    # Return the two different marks
    return sum(mark_privilege_0)/maximum_mark, sum(mark_privilege_1)/maximum_mark


def defense(pos, pieces_0, pieces_1, side):
    """Evaluates how well defended are the kings and the winning squares"""

    # Get the squares around the kings
    i, j = int(pieces_0[0][0]), int(pieces_0[0][1])
    squares_around_king_0 = [str(i+x) + str(j+y) for x in [0, 1, -1] for y in [0, 1, -1] if i+x <= 4 and i+x >= 0 and j+y <= 4 and j+y >= 0]

    i, j = int(pieces_1[0][0]), int(pieces_1[0][1])
    squares_around_king_1 = [str(i+x) + str(j+y) for x in [0, 1, -1] for y in [0, 1, -1] if i+x <= 4 and i+x >= 0 and j+y <= 4 and j+y >= 0]

    # Count how many of them are defended and normalize
    defense_king_0 = 0
    maximum = 0
    for square in squares_around_king_0:
        for p in next_positions(pos, false_side = (side == 1)):
            if square in divide(p, only_pieces=True)[0]:
                defense_king_0 += 1
            
            maximum += 1

    defense_king_0 /= maximum

    defense_king_1 = 0
    maximum = 0
    for square in squares_around_king_1:
        for p in next_positions(pos, false_side = (side == 0)):
            if square in divide(p, only_pieces=True)[1]:
                defense_king_1 += 1
            
            maximum += 1

    defense_king_1 /= maximum

    # Do the same for the 2 winning squares
    i, j = 2, 0
    squares_around_loosing_square_0 = [str(i+x) + str(j+y) for x in [0, 1, -1] for y in [0, 1, -1] if i+x <= 4 and i+x >= 0 and j+y <= 4 and j+y >= 0]

    i, j = 2, 4
    squares_around_loosing_square_1 = [str(i+x) + str(j+y) for x in [0, 1, -1] for y in [0, 1, -1] if i+x <= 4 and i+x >= 0 and j+y <= 4 and j+y >= 0]

    # Count how many of them are defended and normalize
    defense_square_0 = 0
    maximum = 0
    for square in squares_around_loosing_square_0:
        for p in next_positions(pos, false_side = (side == 1)):
            if square in divide(p, only_pieces=True)[0]:
                defense_square_0 += 1
            
            maximum += 1

    defense_square_0 /= maximum

    defense_square_1 = 0
    maximum = 0
    for square in squares_around_loosing_square_1:
        for p in next_positions(pos, false_side = (side == 0)):
            if square in divide(p, only_pieces=True)[1]:
                defense_square_1 += 1
            
            maximum += 1

    defense_square_1 /= maximum

    # Quantify the importance of the different components of the defense mark
    mark_defense_0 = int(pieces_1[0][1])*defense_square_0/4 + defense_king_0*(len(pieces_1) - 1)/4
    mark_defense_1 = int(pieces_0[0][1])*defense_square_1/4 + defense_king_1*(len(pieces_0) - 1)/4

    # Make the 1 a -1, let the 0 be a zero
    return (mark_defense_0 - mark_defense_1)/5

    
def update_dict(pos, mark):
    """Updates the position_values dictionary"""

    # Add the position to the dictionary
    positions_values.update({pos : (mark, 0)})

    # Add its diagonally-symmetric position
    positions_values.update({diagonal_symmetry(pos):(-mark, 0)})

    # Add also the horizontally-symmetric and horizontally-diagonally-simmetric positions
    h_pos = horizontal_symmetry(pos)
    positions_values.update({h_pos:(mark, 0)})
    positions_values.update({diagonal_symmetry(h_pos):(-mark, 0)})


def can_win_other_side(pos, side, old_pieces):
    """Evaluates if the other side can win at the next move"""

    # For every possible position (if the playing side wastes a move)
    for pp in next_positions(pos, false_side = True):

        # Get the new pieces
        new_pieces = divide(pp, only_pieces = True)

        # Did the correctly-playing side lose their king?
        if (old_pieces[side^1][0] != new_pieces[side^1][0]):

            # Return the answer
            return True


def evaluate(pos):
    """Evaluates a position and returns the mark"""
    # If the position is already in the database return its value
    if pos in positions_values:
        return positions_values[pos][0]

    # Divide the position into pieces and cards
    pieces_0, cards_0, pieces_1, cards_1 = divide(pos)

    # Understand who has to play (0: white, 1: black)
    side = int(len(cards_0) < len(cards_1))

    # If you already reached the winning square return +/-inf
    if [pieces_0, pieces_1][side][0] == ("2" + str(4-side*4)):

        # Make the 1 a -1 and the 0 a 1
        mark = (1 - 2*side)*int("inf")

        # Update the database
        update_dict(pos, mark)

        return mark

    # If the other side reached the winning square return -/+inf
    elif [pieces_0, pieces_1][side^1][0] == ("2" + str(4-(side^1)*4)):

        # Make the 1 a -1 and the 0 a 1. Then change the sign
        mark = -(1 - 2*side)*int("inf")

        # Update the database
        update_dict(pos, mark)

        return mark

    # If you can reach the winning square or kill the opposite king (on the next move) return +/-inf
    elif will_win(pos, side, [pieces_0, pieces_1]):

        # Make the 1 a -1 and let the 0 be a 0
        mark = (1 - 2*side)*float('inf')

        # Update the database
        update_dict(pos, mark)

        return mark

    # If the other king can reach the winning square or kill your king (on the next move) return -/+inf
    elif will_win(pos, side^1, [pieces_0, pieces_1], other_side = True, false_side = True):

        # Make the 1 a -1 and let the 0 be a 0
        mark = -(1 - 2*side)*float('inf')

        # Update the database
        update_dict(pos, mark)

        return mark

    # If the other side can win at the next move (but you can do something about it)
    elif can_win_other_side(pos, side^1, [pieces_0, pieces_1]):

        # Find all possible moves
        possible_moves = next_positions(pos)

        print(filler, "\n", pos, "\n", filler,"\n")
        # Evaluate them
        for p in possible_moves:
            blockPrint()
            print(p, "=", evaluate(p))
            enablePrint()

        # Now sort them by score
        possible_moves.sort(key = lambda x: positions_values[x][0], reverse = side)
        print(dict(zip(possible_moves, [positions_values[i][0] for i in possible_moves])))

        # And assign the maximum (or minimum, if side = 1) to the marks
        mark = positions_values[possible_moves[0]][0]

        # Update the database
        update_dict(pos, mark)

        return mark

    # Define the variable
    mark = 0

    # Give a mark according to a material balance
    mark_material = [(len(pieces_0)-1)/4, (len(pieces_1)-1)/4]
    print("\nMark", mark, "Mark_Material", mark_material)

    # Combine centrality and material
    mark_centrality = centrality(pos, pieces_0, pieces_1)
    print("Mark", mark, "Mark_Centrality", mark_centrality)
    mark += ((1.25 - mark_material[1])*mark_centrality[0] - (1.25 - mark_material[0])*mark_centrality[1])

    # Add the domination mark
    mark_domination = domination(pos, pieces_0, pieces_1)
    print("Mark", mark, "Mark_Domination", mark_domination)
    mark += (mark_domination[0]*(1.25 - mark_material[1]) - mark_domination[1]*(1.25 - mark_material[0]))

    if mark != 0:

        temporary_mark = 1

        # Evaluate the control
        mark_control = control(pos, side)

        # Combine it with the material mark
        mark_control = (mark_control[0]*(1.25 - mark_material[1]) - mark_control[1]*(1.25 - mark_material[0]))
        print("Temporary_Mark", temporary_mark, "Mark_Control", mark_control)

        if mark_control != 0:

            # Check if the sign of mark and of mark_control is the same
            exponent = int(mark/mark_control > 0)

            # Make the 0 a -1 but let the 1 be a 1
            exponent = -1 + 2*exponent

            # If they have the same sign multiply by mark_control, otherwise divide
            temporary_mark *= (1 + abs(mark_control))**exponent

        # Evaluate the protection
        mark_protection = protection(pos, side, [pieces_0, pieces_1])
        print("Temporary_Mark", temporary_mark, "Mark_Protection", mark_protection)

        if mark_protection != 0:

            # Check if the sign of mark and of mark_control is the same
            exponent = int(mark/mark_protection > 0)

            # Make the 0 a -1 but let the 1 be a 1
            exponent = -1 + 2*exponent

            # If they have the same sign multiply by mark_control, otherwise divide
            temporary_mark *= (1 + abs(mark_protection))**exponent
        
        # Evaluate the privilege
        mark_privilege = privilege(pos, [cards_0, cards_1])
        
        # Combine it with the material mark
        mark_privilege = (mark_privilege[0]*(1.25 - mark_material[1]) - mark_privilege[1]*(1.25 - mark_material[0]))/2
        print("Temporary_Mark", temporary_mark, "Mark_Privilege", mark_privilege)

        if mark_privilege != 0 :

            # Check if the sign of mark and of mark_privilege is the same
            exponent = int(mark/mark_privilege > 0)

            # Make the 0 a -1 but let the 1 be a 1
            exponent = -1 + 2*exponent

            # If they have the same sign multiply by mark_privilege, otherwise divide
            temporary_mark *= (1 + abs(mark_privilege))**exponent

        # Evaluate the defense
        mark_defense = defense(pos, pieces_0, pieces_1, side)
        print("Temporary_Mark", temporary_mark, "Mark_Defense", mark_defense)

        if mark_defense != 0:

            # Check if the sign of mark and of mark_privilege is the same
            exponent = int(mark/mark_defense > 0)

            # Make the 0 a -1 but let the 1 be a 1
            exponent = -1 + 2*exponent

            # If they have the same sign multiply by mark_privilege, otherwise divide
            temporary_mark *= (1 + abs(mark_defense))**exponent

        denominator = max([1, int(mark_protection != 0) + int(mark_privilege != 0) + int(mark_defense != 0) + int(mark_control)])
        mark *= temporary_mark**(1/denominator)

    # Make all -0 into 0
    if abs(mark) == 0:
        mark = 0

    # If the mark is small
    elif abs(mark) <= 0.45 :

        # And if the best side is not the one with the move
        if (mark > 0) == side :

            # Return half the mark
            mark *= 0.5

    # Round the mark
    mark = round(mark, 1)

    # Update positions' dictionary
    update_dict(pos, mark)

    return mark


class Board:

    background = numpy.array([[" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "],
                              [" ", " ", " ", " ", " "]])

    board = copy.deepcopy(background)
    cards_0 = []
    cards_1 = []
    position = ""

    def __init__(self, position):

        self.position = position
        self.update_stuff()
        self.show()
      
    def update_stuff(self):
        """Updates the board and the cards"""

        pieces_0, cards_0, pieces_1, cards_1 = divide(self.position)

        self.board = copy.deepcopy(self.background)
        self.board[4 - int(pieces_0[0][1])][int(pieces_0[0][0])] = "B"
        self.board[4 - int(pieces_1[0][1])][int(pieces_1[0][0])] = "N"
        self.cards_0 = []
        self.cards_1 = []

        if len(pieces_0) > 1:
            for p in pieces_0[1::] :
                self.board[4 - int(p[1])][int(p[0])] = "b"

        if len(pieces_1) > 1:
            for p in pieces_1[1::] :
                self.board[4 - int(p[1])][int(p[0])] = "n"

        for card, i in zip(cards_0, range(len(cards_0))) :
            self.cards_0.append(copy.deepcopy(self.background))
            self.cards_0[i][2][2] = "P"
            
            for move in cards[card] :
                self.cards_0[i][2 - move[1]][2 + move[0]] = "O"
        
        for card, i in zip(cards_1, range(len(cards_1))) :
            self.cards_1.append(copy.deepcopy(self.background))
            self.cards_1[i][2][2] = "P"
            
            for move in cards[card] :
                self.cards_1[i][2 + move[1]][2 - move[0]] = "O"

    def show(self):

        print(filler)
        print(self.position, "=", positions_values[self.position][0])
        print(filler, "\n")
    
        self.cards_1.reverse()
        for c in self.cards_1:
            print(c, "\n")

        print(filler, "\n")
        print(self.board, "\n")
        print(filler, "\n")

        for c in self.cards_0:
            print(c, "\n")

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__
                
# ----------------------------------------------------------------------------------------------------------------------
# User inputs
# ----------------------------------------------------------------------------------------------------------------------

# Get user inputs
if len(sys.argv) != 1 and len(sys.argv) != 6:
    white_cards = ["a", "b", "c"]
    black_cards = ["d", "e"]

elif len(sys.argv) == 1:

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
                if c not in list(cards.keys()) :
                    print("\nInvalid input: select 5 different cards from the list and write them like this 'a b c d e'")
                    condition = True
                    break

            white_cards = input_cards[0:3]
            black_cards = input_cards[3:5]

        else:
            print("\nInvalid input: select 5 different cards from the list and write them like this 'a b c d e'")

else :
    white_cards = sys.argv[1:4]
    black_cards = sys.argv[4:6]

# ----------------------------------------------------------------------------------------------------------------------
# Data and Memory Allocation
# ----------------------------------------------------------------------------------------------------------------------

# Starting position
pos = "2000103040{}2404143444{}".format("".join(white_cards), "".join(black_cards))

# ----------------------------------------------------------------------------------------------------------------------
# Gameplay
# ----------------------------------------------------------------------------------------------------------------------

'''
all_pos = []
for p in next_positions(pos):
    for n in next_positions(p):
        for m in next_positions(n):
            evaluate(m)
            all_pos.append(m)

with open(r"C:\Desktop\dict_onitama.pkl", "wb") as file:
        pickle.dump(positions_values, file)

all_pos.sort(key = lambda x : positions_values[x][0], reverse = True)
for p in all_pos[0:10] + all_pos[-10:-1]:
    x = Board(p)
    '''

p = "2200102130ce2304143444dba"
#blockPrint()
evaluate(p)
#enablePrint()
x = Board(p)

'''
positions_values = {}

p = diagonal_symmetry(p)
blockPrint()
evaluate(p)
enablePrint()
x = Board(p)
'''

# ----------------------------------------------------------------------------------------------------------------------
# Graphical Post-Processing
# ----------------------------------------------------------------------------------------------------------------------


# à DOVRESTI ANCHE VALUTARE SE ALLA PROSSIMA MOSSA L'ALTRO GIOCATORE
# PUò FARE UNA MOSSA CHE LO METTE IN UNA POSIZIONE IN CUI VINCE PER FORZA. ED ANCHE IN QUEL CASO 
# CAN_WIN_OTHER_SIDE DOVREBBE RITORNARE TRUE:
# INFATTI DEVI IMPEDIRGLI NECESSARIAMENTE DI FARE QUELLA MOSSA. DUNQUE BISOGNA VALUTARE SULLA PROSSIMA POSIZIONE
