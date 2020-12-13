"""
This is explained in our README, too. But we noticed that certain aspects seemed to be uniform
and reusable across different files. Therefore, we placed them in this constants file in order
to not use any magic numbers.
"""
TILE_SIZE = 40

# Our tiles accommodate up to 7 fish per tile if the tile size is <=40, which is what we deem an acceptable tile size
MAX_FISH = 7

FISH_SIZE = 2*(TILE_SIZE-10) / MAX_FISH

PENGUIN_SIZE = 1.5*FISH_SIZE

PENGUIN_COLORS = ['red', 'white', 'brown', 'black']
