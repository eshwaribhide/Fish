from strategy import Strategy

# how many turns to look ahead in the game tree when determining the best action to take
TURNS_LOOK_AHEAD = 2

"""
A Player is an object that exists to provide the game-playing logic of placing and moving avatars, so the Referee will
call the player interface methods at the appropriate time. A player will not actually do the placing or the moving, 
so as not to directly manipulate the official game state, and the return values of the place_avatar or move_avatar
functions will be first checked by the referee and then used to make the placement or the move. 

A Player can exist for multiple games in a tournament and maybe even multiple tournaments. So, in order to uniquely
identify the player throughout my whole codebase, the player has an attribute called player_id, which is an int. 

An Action is a tuple of the form ((start_row, start_col), (dest_row, dest_col)). 
Where *row, and *col are both ints. (start_row, start_col) is the current location of a penguin, and (dest_row, dest_col) 
is the location that the penguin wants to go to. See board.py for details on the coordinate system. An empty Action, 
representing a time when a Player cannot make a move, is of the form ().
"""


class Player:

    def __init__(self, player_id):
        self.__player_id = player_id
        self.__game_is_ongoing = False

    def game_has_started(self):
        self.__game_is_ongoing = True

    def game_has_ended(self):
        self.__game_is_ongoing = False

    def place_avatar(self, current_game_state):
        return Strategy(current_game_state, self.__player_id).zig_zag()

    def move_avatar(self, current_game_state):
        return Strategy(current_game_state, self.__player_id).which_action_to_take(TURNS_LOOK_AHEAD)

    def get_player_id(self):
        return self.__player_id
