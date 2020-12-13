"""
Interface for a player.
In [row,col], row and col are both ints, 0-based. See board.py for my coordinate system.
"""

"""
Nothing -> Nothing
This tells a Player that the game has started, by setting their game_is_ongoing flag to True.
"""
def game_has_started():
    pass


"""
Nothing -> Nothing
This tells a Player that the game has ended, by setting their game_is_ongoing flag to True.
"""
def game_is_over():
    pass


"""
GameState -> [int, int]
This method will ask the player to return the position [row,col] where row and col are both ints for where
the player wants to place their penguin. See board.py for details on the coordinate system.
"""
def place_avatar():
    pass


"""
GameState -> Action
This method will ask the player to return the Action it wants to take. 
"""
def move_avatar():
    pass


"""
Nothing -> int
Getter method for the player id attribute.
"""
def get_player_id():
    pass

