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

In order to make sure that the 
player does not directly manipulate the game state, the player will not be actually doing the placing or the moving; 
the return type of player place_avatar and move_avatar will 
be the requested placement or action, and if that placement position or action is legal, then the referee will ask 
the game state to execute it. The referee is therefore in charge of catching any abnormal interactions between the 
referee and a player and eliminating the player if it does this.

Abnormal interactions between Referee and Player:
- Gives a data structure other than the expected data structure for the phase it is in. For placement phase, exp structure
is a List, and for moving phase, exp structure is a tuple. 
- Gives illegal placements/actions.
"""


class Referee:
    # test board is a Board used only for unit testing purposes. For all other cases, it will not be passed in. If it is passed
    # in though, I don't see a need for board_rows and board_columns so they're initialized to None.
    def __init__(self, player_seq, board_rows=None, board_columns=None, test_board=None):
        # a List of Player objects, already in playing order
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

    def __setup(self):
        board = self.__create_board() if self.__test_board is None else self.__test_board
        player_ids = [player.get_player_id() for player in self.__player_seq]
        player_penguin_colors = {player_id: PENGUIN_COLORS[i] for i, player_id in enumerate(player_ids)}
        self.__current_game_state = GameState(board, player_penguin_colors, player_ids)

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

    @staticmethod
    def __get_rand_val(min, max):
        return random.randint(min, max)

    def __get_max_num_tiles_with_attr(self, attr_percentage):
        total_tiles = self.__board_rows * self.__board_columns
        return math.ceil((attr_percentage / 100) * total_tiles)

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

    def __place_or_move_avatar(self, current_player, phase_type):
        return current_player.place_avatar(self.__current_game_state) if phase_type == PLACEMENT \
            else current_player.move_avatar(self.__current_game_state)

    @staticmethod
    def __invalid_structure(structure, exp_structure_type):
        return not isinstance(structure, exp_structure_type) or len(structure) != 2

    def __is_illegal(self, to_execute, phase_type):
        return self.__is_illegal_placement(to_execute) if phase_type == PLACEMENT else self.__is_illegal_action(to_execute)

    def __is_illegal_placement(self, placement):
        return self.__current_game_state.is_pos_out_of_bounds(placement) or \
               not self.__current_game_state.is_unoccupied(placement) or \
               self.__current_game_state.is_hole(placement)

    def __is_illegal_action(self, action):
        game_tree = GameTree(self.__current_game_state)
        game_tree.next_layer()
        return action not in game_tree.get_map_action_to_child_nodes()

    def __remove_player(self, player):
        self.__current_game_state.remove_player(player.get_player_id())
        self.__bad_players.append(player)

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

    def get_player_seq(self):
        return self.__player_seq

    def get_board_rows(self):
        return self.__board_rows

    def get_board_columns(self):
        return self.__board_columns

    def get_current_game_state(self):
        return self.__current_game_state

    def get_bad_players(self):
        return self.__bad_players
