from onitama.evaluation.position import Position
from onitama.interface.constants import WIDTH_BOARD, HEIGHT_BOARD, COLOR_SELECTED_PIECE, PURPLE,COLOR_VALID_CAPTURE, COLOR_VALID_MOVES, WIDTH, HEIGHT, SQUARE_SIZE, DRAW_VALID_MOVES, SIZE_VALID_MOVES
import sys
import time

depth = int(sys.argv[1])

# Starting position
white_cards = ["a", "b", "c"]
black_cards = ["d", "e"]
pos = "2404143444{}2000103040{}".format("".join(black_cards), "".join(white_cards))

pos = Position(pos, 1)

t0 = time.process_time()
pos.find_best_move(depth)
t1 = time.process_time()


print('\nValue = {}, enlapsed in {:.2f} [s]'.format(pos.value, t1 - t0))
print(f'Best move: {pos.best_move}')
print(f'Number of different positions evaluated: {len(list(pos.current_tree.values()))}')