import sys
sys.path.append('../Common')
from board import Board
from tile_fish_penguin_constants import MAX_FISH, PENGUIN_COLORS
from state import GameState
from game_tree import GameTree
import random
import math

RAND_VAL_LOW = 0
RAND_VAL_HIGH = 5
HOLES_MAX_PERCENT = 10
MIN_NUM_ONE_FISH_TILES_MAX_PERCENT = 5
PLACEMENT = "placement"
MOVING = "moving"

"""
A PhaseType is one of PLACEMENT OR MOVING (SEE ABOVE).

A Placement is a List of the form [row, col] where row and col are both ints. See board.py for details on the coordinate system.

An Action is a tuple of the form ((start_row, start_col), (dest_row, dest_col)). 
Where *row, and *col are both ints. (start_row, start_col) is the current location of a penguin, and (dest_row, dest_col) 
is the location that the penguin wants to go to. See board.py for details on the coordinate system.

An Outcome is a Dictionary of the form {"won": List of Player objects, "lost": List of Player objects, 
"cheated/failed": List of Player objects}.

A Referee is an object created SOLELY FOR AN INSTANCE OF A SPECIFIC GAME (IT WON'T BE REUSED). 
It supervises/runs a Fish game, given a list of players ordered by age and dimensions of the board, and then reports the 
game outcome once the game is over.

IN ORDER TO MAKE SURE THAT THE 
PLAYER DOES NOT DIRECTLY MANIPULATE THE GAME STATE, THE PLAYER WILL NOT BE ACTUALLY DOING THE PLACING OR THE MOVING; 
THE RETURN TYPE OF PLAYER PLACE_AVATAR AND MOVE_AVATAR WILL 
BE THE REQUESTED PLACEMENT OR ACTION, AND IF THAT PLACEMENT POSITION OR ACTION IS LEGAL, THEN THE REFEREE WILL ASK 
THE GAME STATE TO EXECUTE IT. THE REFEREE IS THEREFORE IN CHARGE OF CATCHING ANY ABNORMAL INTERACTIONS BETWEEN THE 
REFEREE AND A PLAYER AND ELIMINATING THE PLAYER IF THEY DO THIS.

Abnormal interactions between Referee and Player:
- Gives a data structure other than the expected data structure for the phase it is in. For placement phase, exp structure
is a List, and for moving phase, exp structure is a tuple. 
- Gives illegal placements/actions.
"""

# Class Signature: player_seq is a List of Player objects, board_rows is an int, board_columns is an int


class Referee:
    # test board is a Board used only for unit testing purposes. For all other cases, it will not be passed in. If it is passed
    # in though, I don't see a need for board_rows and board_columns so they're initialized to None.
    def __init__(self, player_seq, board_rows=None, board_columns=None, test_board=None):
        # a List of Player objects, already in the order that they will play in
        self.__player_seq = player_seq
        # an int
        self.__board_rows = board_rows
        # an int
        self.__board_columns = board_columns
        # a Board only used to test the behavior in unit tests
        self.__test_board = test_board
        # The referee's official GameState
        self.__current_game_state = None
        # a List of failing/cheating Players
        self.__bad_players = []

    """
    Nothing -> Outcome (see above for Outcome data def)
  
    This method will be called by the tournament manager, and will basically run the whole Fish game. At the end,
    the outcome of the game will be reported. The handle_phase methods will take care of placement phase and
    moving phase and also handle instances of cheating/failing players.
    """
    def run_game(self):
        # setup the board, assign the penguin colors to each player, and initialize the current GameState
        self.__setup()
        while not self.__current_game_state.is_game_over() and not self.__current_game_state.is_placement_phase_over():
          # the expected type of a Placement is a List (see handle_phase function for more info)
            self.__handle_phase(PLACEMENT, list)
        while not self.__current_game_state.is_game_over():
          # the expected type of an Action is a tuple (see handle_phase function for more info)
            self.__handle_phase(MOVING, tuple)
        return self.__report_outcome()

    """
    Nothing -> Nothing
    Creates a random board, assigns colors to each player, and then initializes the current GameState. In a GameState,
    players are all referenced by their unique player ids (see player.py for more info on this concept).
    """
    def __setup(self):
        board = self.__create_board() if self.__test_board is None else self.__test_board
        player_ids = [player.get_player_id() for player in self.__player_seq]
        # penguin color assignment
        player_penguin_colors = {player_id: PENGUIN_COLORS[i] for i, player_id in enumerate(player_ids)}
        self.__current_game_state = GameState(board, player_penguin_colors, player_ids)

    """
    Nothing -> Board object
    Creates a random board. There is no real logic to this...I just wanted a variety of different Boards to be
    present. Based on random values that are generated, certain attributes of the board are determined (how many/where
    the holes are, whether there is a min num of one fish tiles, or whether there is a set num of fish per tile).
    """
    def __create_board(self):
        rand_val = self.__get_rand_val(RAND_VAL_LOW, RAND_VAL_HIGH)

        if rand_val == RAND_VAL_LOW:
            board = Board(self.__board_rows, self.__board_columns, {})
        else:
            holes = self.__create_board_holes()
            if rand_val % 2 == 0:
                board = Board(self.__board_rows, self.__board_columns, holes,
                              min_num_one_fish_tiles=
                              self.__get_rand_val(RAND_VAL_LOW,
                                                  self.__get_max_num_tiles_with_attr(MIN_NUM_ONE_FISH_TILES_MAX_PERCENT)))
            elif rand_val == RAND_VAL_HIGH:
                board = Board(self.__board_rows, self.__board_columns, holes,
                              num_fish_per_tile=self.__get_rand_val(RAND_VAL_LOW, MAX_FISH))
            else:
                board = Board(self.__board_rows, self.__board_columns, holes)
        return board

    """
    Nothing -> {row: [col]} where row and col are both ints. So a hole at [1, 2] would have 1 as its key and in the
    value for that key, which is a List, 2 would be present. See board.py for more information.
    
    Determines how many/where the holes are on the board. Again, there is no real logic to this...I just determine
    these things based on random numbers that are generated.
    """
    def __create_board_holes(self):
        num_holes = self.__get_rand_val(RAND_VAL_LOW, self.__get_max_num_tiles_with_attr(HOLES_MAX_PERCENT))
        count = 0
        holes = {}

        while count < num_holes:
            rand_row = self.__get_rand_val(RAND_VAL_LOW, self.__board_rows - 1)
            rand_col = self.__get_rand_val(RAND_VAL_LOW, self.__board_columns - 1)

            if rand_row not in holes:
                holes[rand_row] = [rand_col]
            elif rand_col not in holes[rand_row]:
                holes[rand_row].append(rand_col)
            else:
                continue
            count += 1

        return holes

    """
    int int -> int
    Helper method to generate a random value x, where min <= x <= max.
    """
    @staticmethod
    def __get_rand_val(min, max):
        return random.randint(min, max)

    """
    int -> int
    Given a max percentage for an attribute, determines how many tiles on the board can have that attribute
    (so either holes or one fish tiles).
    """
    def __get_max_num_tiles_with_attr(self, attr_percentage):
        total_tiles = self.__board_rows * self.__board_columns
        return math.ceil((attr_percentage / 100) * total_tiles)

    """
    PhaseType List -> Nothing (if phase_type is PLACEMENT). Since type of a Placement is a List. 
    PhaseType Tuple -> Nothing (if phase_type is MOVING). Since type of an Action is a tuple.
    See top of this file where Placements and Actions are described more in detail. 
    
    Handles either a placement or moving phase by having the player give their placement or action, checking first whether the player
    actually submitted only a Placement when they were supposed to or only an Action when they were supposed to, and whether
    it is legal (if illegal then eliminates the player), and then having the game state do the placement or action. The
    phase type comes into play in order to be able to do phase-specific checks. If a placement/move is illegal, then
    the player is eliminated from the game, and is added to the referee's bad_players list.
    
    Also, the player will be eliminated if they don't respond after a time limit or crash/malfunction, which I will
    add in the future when we deal with remote players. See the top of this file for more detail on what I deem abnormal 
    interactions.
    """
    def __handle_phase(self, phase_type, exp_structure_type):
        # in order to cycle shift player sequence
        current_player = self.__player_seq.pop(0)
        to_execute = self.__place_or_move_avatar(current_player, phase_type)
        if phase_type == MOVING and to_execute == ():
            self.__current_game_state.skip_turn(current_player.get_player_id())
        else:
            if self.__invalid_structure(to_execute, exp_structure_type) or self.__is_illegal(to_execute, phase_type):
                self.__remove_player(current_player)
            else:
                self.__current_game_state.place_avatar(current_player.get_player_id(), to_execute) \
                    if phase_type == PLACEMENT else \
                    self.__current_game_state.move_avatar(current_player.get_player_id(), list(to_execute[0]), list(to_execute[1]))
                # tacks this on to the end of the player sequence, cycle shift of player sequence
                self.__player_seq.append(current_player)

    """
    Player PhaseType -> Placement (if phase_type is PLACEMENT)
    Player PhaseType -> Action (if phase_type is MOVING)
    Asks the player to return either where they want to place an avatar or what Action they want to take, based
    on the phase type.
    """
    def __place_or_move_avatar(self, current_player, phase_type):
        return current_player.place_avatar(self.__current_game_state) if phase_type == PLACEMENT \
            else current_player.move_avatar(self.__current_game_state)

    """
    Some Data Structure, List -> Boolean
    Some Data Structure, Tuple -> Boolean (List or Tuple are the only possible data types, List is the data type of a Placement, 
    Tuple is the data type of an Action)
    
    Returns True if structure is not as expected and False if it is. Helps catch the cases when a Player submits an 
    Action, for example, when the placement phase is going on. Or maybe the player malfunctions and gives some random 
    data structure.
    
    The len=2 check is because if you see the data def for a Placement, the List has 2 elements, a row and a col. For an Action, 
    if you see the data def...the tuple has 2 tuples inside of it, representing start and destination positions.
    """
    @staticmethod
    def __invalid_structure(structure, exp_structure_type):
        return not isinstance(structure, exp_structure_type) or len(structure) != 2

    """
    Placement, PhaseType -> Boolean
    Action, PhaseType -> Boolean
    Returns true if "to_execute", which always will be either of type Placement or Action, is illegal, and False if not.
    """
    def __is_illegal(self, to_execute, phase_type):
        return self.__is_illegal_placement(to_execute) if phase_type == PLACEMENT else self.__is_illegal_action(to_execute)

    """
    Placement -> Boolean
    Returns true if the given Placement is illegal (out of bounds, is occupied, or is a hole) and False if not.
    """
    def __is_illegal_placement(self, placement):
        return self.__current_game_state.is_pos_out_of_bounds(placement) or \
               not self.__current_game_state.is_unoccupied(placement) or \
               self.__current_game_state.is_hole(placement)

    """
    Action -> Boolean
    Returns true if the given Action is illegal (it's not in the GameTree's map of Actions to child nodes) and False if not.
    """
    def __is_illegal_action(self, action):
        game_tree = GameTree(self.__current_game_state)
        game_tree.next_layer()
        return action not in game_tree.get_map_action_to_child_nodes()

    """
    Player -> Nothing
    Removes a Player from the game by calling the GameState remove player method, which removes all a Player's penguins
    and any of the Player's information from the GameState. The Player DOES NOT get removed from the Referee's knowledge.
    It will be saved in the referee's list of "bad players" in order to be reported at the end of the game. 
    """
    def __remove_player(self, player):
        self.__current_game_state.remove_player(player.get_player_id())
        self.__bad_players.append(player)

    """
    Nothing -> Outcome
    Reports who won, who lost, and who cheated or failed. I don't think it's necessary to report the actual scores, as
    I do not see how the tournament manager would be using this information, especially since most likely the 
    tournaments will be run in a round-robin format (everyone plays against everyone). What's most important here is
    the winners, as this information will be needed in who won a tournament (since that depends on who won the most games), 
    and also the cheating/failing players because they cannot play again or sign up for a tournament again. I still wanted to report the losers anyways. 
    """
    def __report_outcome(self):
        outcome = {"won": [], "lost": [], "cheated/failed": self.__bad_players}
        winning_score = self.__current_game_state.get_winning_score()
        for player in self.__player_seq:
            if player not in self.__bad_players:
                if self.__current_game_state.get_player_score(player.get_player_id()) == winning_score:
                    outcome["won"].append(player)
                else:
                    outcome["lost"].append(player)
        return outcome

    """
    Nothing -> [Player]
    Getter method for the player seq attribute.
    """
    def get_player_seq(self):
        return self.__player_seq

    """
    Nothing -> int
    Getter method for the board rows attribute.
    """
    def get_board_rows(self):
        return self.__board_rows

    """
    Nothing -> int
    Getter method for the board columns attribute.
    """
    def get_board_columns(self):
        return self.__board_columns

    """
    Nothing -> GameState
    Getter method for the current game state attribute.
    """
    def get_current_game_state(self):
        return self.__current_game_state

    """
    Nothing -> [Player]
    Getter method for the bad players attribute.
    """
    def get_bad_players(self):
        return self.__bad_players
