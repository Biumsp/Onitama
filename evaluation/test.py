from evaluation import Position
import os

# Starting position
white_cards = ["a", "b", "c"]
black_cards = ["d", "e"]
pos = "2404143444{}2000103040{}".format("".join(black_cards), "".join(white_cards))
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pos = Position(pos, 1, WIN)
pos.evaluate(3)

print(pos.value)
for p in list(pos.current_tree.values()):
    print(p.value)