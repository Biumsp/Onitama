
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

def privilege(pos):
    """Evaluates the presence of cards with a distinctive move"""

    mark_privilege_0, mark_privilege_1 = [], []

    all_cards = pos.cards[0] + pos.cards[1]
    
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

    for c in all_cards:
        partial_mark = 0

        for m in cards[c]:
            partial_mark += (dict_moves[m])

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
            if c in pos.cards[i]:

                # Add the normalized position of the card in the all_card list to the correct mark-variable
                marks_privilege[i].append(marks_cards[c]/maximum_mark)

    # Get the maximum mark that was given to a side
    maximum_mark = max([sum(m) for m in marks_privilege])

    # Return the two different marks
    return sum(mark_privilege_0)/maximum_mark, sum(mark_privilege_1)/maximum_mark


def domination(pos):
    """Evaluates how each side restrictes the other"""
    
    # Initiate variables
    mark_domination_0, mark_domination_1 = 0, 0
    
    # Give a point for every piece y-position
    for piece in pos.pieces[1]:

        # But give it only if the opposite king is restricted 
        if int(piece[1]) <= int(pos.pieces[0][0][1]):
            mark_domination_1 += int(piece[1])

    # Give a point for every piece y-position
    for piece in pos.pieces[0]:

        # But give it only if the opposite king is restricted 
        if int(piece[1]) >= int(pos.pieces[1][0][1]):
            mark_domination_0 += (4- int(piece[1]))

    # Normalize by the maximum you can get
    return mark_domination_0/15, mark_domination_1/15


def centrality(pos):
    """Evaluates how central the pieces of each side are"""
    
    # Initiate variables
    centrality_mark_0, centrality_mark_1 = 0, 0

    # Give a mark to every piece
    for piece in pos.pieces[0]:

        # The more central the piece, the higher the mark
        centrality_mark_0 += (2 - abs(2 - int(piece[0])))*(2 - abs(2 - int(piece[1])))

    # Give a mark to every piece
    for piece in pos.pieces[1]:

        # The more central the piece, the higher the mark
        centrality_mark_1 += (2 - abs(2 - int(piece[0])))*(2 - abs(2 - int(piece[1])))

    # Normalize by the number of pieces of each side (we want an intensive parameter)
    centrality_mark_0 *= 1/len(pos.pieces[0])
    centrality_mark_1 *= 1/len(pos.pieces[1])
    
    # Divide by 4 for normalization
    return centrality_mark_0/4, centrality_mark_1/4


def evaluate_pos(pos):
    """Evaluates a position and returns the mark"""

    if not pos.next_pos:
        pos._get_next_pos()

    mark = 0

    mark_material = [(len(pos.pieces[0])-1)/4, (len(pos.pieces[1])-1)/4]
    #print("\nMark", mark, "Mark_Material", mark_material)

    mark_centrality = centrality(pos)
    #print("Mark", mark, "Mark_Centrality", mark_centrality)
    mark += ((1.25 - mark_material[0])*mark_centrality[1] - (1.25 - mark_material[1])*mark_centrality[0])

    mark_domination = domination(pos)
    #print("Mark", mark, "Mark_Domination", mark_domination)
    mark += (mark_domination[1]*(1.25 - mark_material[0]) - mark_domination[0]*(1.25 - mark_material[1]))

    if mark != 0:
        mark_privilege = privilege(pos)
        mark_privilege = (mark_privilege[1]*(1.25 - mark_material[0]) - mark_privilege[0]*(1.25 - mark_material[1]))/2
        #print("Temporary_Mark", mark, "Mark_Privilege", mark_privilege)

        if mark_privilege != 0 :
            exponent = int(mark/mark_privilege > 0)
            exponent = -1 + 2*exponent
            mark *= (1 + abs(mark_privilege))**exponent

    elif abs(mark) <= 0.45 :
        # And if the best pos.turn is not the one with the move
        if (mark > 0) != pos.turn :
            # Return half the mark
            mark *= 0.5

    # Round the mark
    mark = round(mark, 1)

    if abs(mark) == 0:
        mark = 0

    return mark