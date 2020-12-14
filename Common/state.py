from fish import __Fish as fish_inst
from penguin import __Penguin as penguin_inst
from tile_fish_penguin_constants import TILE_SIZE
import tkinter

"""
A GAME STATE REPRESENTS THE CURRENT STATE OF THE GAME. A GAME STATE HAS INFORMATION ABOUT THE STATE OF
THE BOARD. THIS IS DONE BY HAVING THE GAME STATE CONTAIN A BOARD OBJECT WITHIN IT (SEE BOARD.PY FOR DETAILS).
THIS MEANS THE GAME STATE HAS INFORMATION ABOUT WHAT TILES ARE ON THE BOARD, WHERE THE HOLES ARE ON A BOARD,
HOW MANY FISH ARE ON A TILE, ETC, SIMPLY THROUGH THIS CONTAINMENT OF THE BOARD OBJECT. A GAME STATE
ALSO HAS KNOWLEDGE OF THE PLAYER PENGUIN COLORS, THE ORDER IN WHICH PLAYERS PLAY, WHOSE TURN IT
CURRENTLY IS, HOW MANY FISH EACH PLAYER HAS, AND WHERE EACH PLAYER'S PENGUINS ARE LOCATED.
THE NUMBER OF PLAYERS IS IMPLICITLY DEFINED BY THE LENGTH OF THE PLAYER PENGUIN COLORS DICT/PLAYER ORDER LIST!
SO IT IS NOT PASSED IN AS A PARAMETER!!!
"""

# on the board, this is the x offset for placing a tile. so the leftmost tile will have x of 5..etc. this
# is because when drawing it gets cut off otherwise.
TILE_X_OFFSET = 5

# on the board, this is the y offset for placing a tile. so the leftmost tile will have # y of 10..etc. this
# is because when drawing it gets cut off otherwise.
TILE_Y_OFFSET = 10


class GameState:
    
    def __init__(self, board, player_penguin_colors, player_order,
                 player_fish_count=None, penguin_posns=None):
        # initialized and passed in by the referee. Is a Board object (see board.py) for the data definition
        self.__board = board

        # passed in by the referee, has a setter method in case a player is terminated. Is a dictionary
        # of the form {player_id: player_penguin_color}, where a player_id is an int and a
        # player_penguin_color is a String.
        # It needs to be passed in by the referee because the referee assigns each player the penguin colors.
        self.__player_penguin_colors = player_penguin_colors

        # passed in by the referee, has a setter method in case a player is terminated, so order changes.
        # Is a list of the form [player_id], where a player_id is an int.
        # It needs to be passed in by the referee because the referee has knowledge about the players'
        # ages.
        # I know whose turn it is based on what the first element in this list is. In other words, at the present
        # moment it is will be player_order[0]'s turn
        self.__player_order = player_order

        # maps a player id to the number of fish it has
        # is a Dictionary of the form {int: int}, specifically {player_id: fish_count}
        self.__player_fish_count = player_fish_count if player_fish_count is not None else \
            {player_id: 0 for player_id in self.__player_order}

        # maps a player id to a double nested array containing [row,col] penguin posns
        # is a Dictionary of the form {player_id: [[row,col]]}
        # Where a player id is an int, and row, col are both ints
        self.__penguin_posns = penguin_posns if penguin_posns is not None else {}
        if self.__penguin_posns == {}:
            self.__init_penguin_posns()

    def __init_penguin_posns(self):
        """
        No signature per se, but utilizes the self.__player_penguin_colors var to set the self.__penguin_posns var
        to {player_id: [[row,col]]} (types are {int: [[int, int]]})
        The purpose of this function is to initialize a game state for a given number of players. Specifically,
        as a class variable called 'players' mapping players to their penguin color, the GameState class has
        knowledge about all the players. For now, we can identify a player by their id, which means the length of
        that players variable represents the number of players.
        Here, we create a data structure that maps a player id to a list of its penguin posns.
        We know by the game rules
        that each player receives 6-N penguins, meaning each list of penguin posns has a length of 6-N. As
        placeholders, we set each value at an index to an empty list, but in real gameplay, at each index will be a
        sublist
        of the form [row, col].
        """
        penguin_posns = {}
        num_of_players = len(self.__player_penguin_colors)
        penguins_per_player = 6 - num_of_players

        for player_id in self.__player_penguin_colors:
            penguin_posns[player_id] = [[] for _i in range(penguins_per_player)]

        self.__penguin_posns = penguin_posns

    def is_pos_out_of_bounds(self, posn):
        """
        [int, int] -> bool
        Checks if the selected tile posn is out of bounds.
        :param posn: an list representing row as first val and col as second val
        :returns True if either the row or col val is out of bounds and false if not
        """
        board_rows = self.__board.get_rows()
        board_columns = self.__board.get_columns()

        pos_row = posn[0]
        pos_col = posn[1]

        return (pos_row < 0 or pos_row >= board_rows) or (pos_col < 0 or pos_col >= board_columns)

    def player_has_penguin_at_pos(self, player_id, posn):
        """
        int [int,int] -> bool
        The purpose of this function is to simply verify for a player id, if they have a penguin at a particular
        posn.
        :param player_id: an int that represents a unique player
        :param posn: a List of the form [row, col] where row and col are both ints
        :return True if the player has a penguin at the posn and False if not
        """
        player_penguin_posns = self.__penguin_posns[player_id]
        return posn in player_penguin_posns

    def is_hole(self, posn):
        """
        [int, int] -> bool
        
        Checks whether a particular posn is a hole. 
        :param posn: a List of the form [row, col] where row and col are both ints
        :return: True if the tile is a hole (its visibility is set to False) and False if not
        """
        board_tiles = self.__board.get_tiles()
        pos_row = posn[0]
        pos_col = posn[1]
        tile_at_pos = board_tiles[pos_row][pos_col]

        return not tile_at_pos.get_visibility()

    def is_unoccupied(self, posn):
        """
        [int, int] -> bool
        
        The purpose of this function is to check whether this slot is unoccupied: in other words, that 
        there is no penguin who is currently located at this spot. This is done by making sure the posn
        does not appear in any player's current penguin posns.
        :param posn: a List where the first value represents the row, the second value represents the column
        of a particular posn
        :return: True if no penguin is currently at the posn and False if not
        """
        for player_id in self.__penguin_posns:
            if self.player_has_penguin_at_pos(player_id, posn):
                return False
        return True

    def get_all_reachable_dests_help(self, start_pos, lo_all_penguin_posns, recurse):
        """
        [int, int] [[int, int]] bool -> [[int, int]]
        Helper function for all destinations. Gets all the destinations that a penguin on the start_pos can move to.
        :param start_pos: The posn that a penguin is currently located on, of the form [row, col] where
        row and col are both ints
        :param lo_all_penguin_posns: A list of all the [row,col] posns on which a penguin is located, so the
        board can deem these locations as unreachable
        :param recurse: Will be true if recursion should be done at the end of the board's get_reachable_posns
        method, and False if not
        :return: a List containing all the destination posns of the form [[row, col]] where
        row and col are both ints
        """
        all_destinations = []
        destinations = self.__board.get_reachable_posns(start_pos, lo_all_penguin_posns, recurse)
        for dest_pos in destinations:
            if dest_pos not in all_destinations and self.is_unoccupied(dest_pos):
                all_destinations.append(dest_pos)
        return all_destinations

    def get_all_reachable_dests(self, player_id, which_penguin=None, recurse=True):
        """
        int int bool-> [[int,int]]
        The purpose of this function is to get all reachable posns for a player, for all of their penguins.
        This is public as we use it in the game tree. The parameters which_penguin and recurse were added
        due to the integration tests. Which_penguin is an int. It represents the index for which to select a penguin
        in a player's penguin posns. It represents: which penguin you want to get destinations for. Like, if it is
        0, that means the player's first penguin. If it's 1, the player's second penguin, etc. Since it's 0-indexed.
        Recurse is a flag that is required for the baord's get_reachable_posns method. If you only want to see the
        reachable posns that are one step
        away, then recurse will be set to False. If you want to see all the reachable posns, then
        recurse is True.
        :param player_id:  an int that represents a unique player
        :param which_penguin: an int that represents which penguin to get destinations for.
        :param recurse: Will be true if recursion should be done at the end of the board's get_reachable_posns
        method, and False if not
        :return:a [[row,col]], where row and col are both ints, and [row,col] represents a posn
        on the board.
        """
        player_penguin_posns = self.__penguin_posns[player_id]

        lo_all_penguin_posns = [pp for i in self.__penguin_posns for pp in self.__penguin_posns[i] if pp]

        if which_penguin is not None:
            start_pos = player_penguin_posns[which_penguin]
            all_destinations = self.get_all_reachable_dests_help(start_pos, lo_all_penguin_posns, recurse)
        else:
            all_destinations = []
            for start_pos in player_penguin_posns:
                if start_pos:
                    all_destinations.extend(self.get_all_reachable_dests_help(start_pos, lo_all_penguin_posns, 
                                                                           recurse))
        return all_destinations

    def remove_player(self, player_id):
        """
        int -> Nothing (Void function)
        Removes a player from the game by removing their player id from any of the class variables
        that contain information about the player_id. This is public as the referee can use it
        if a player malfunctions. The most important part of the method is removing the penguins.
        :param player_id:  an int that represents a unique player
        """
        self.__player_penguin_colors.pop(player_id)
        self.__player_order.remove(player_id)
        self.__player_fish_count.pop(player_id)
        self.__penguin_posns.pop(player_id)


    def get_winning_score(self):
        """
        Nothing -> int
        :return: winning score
        """
        return max(self.__player_fish_count.values())

    def get_player_score(self, player_id):
        """
        int -> int
        This method returns the score for a particular player. It is public because we will probably
        need to display it in our final GUI, and also other players may want to know it to see
        where they stand.
        :param player_id:  an int that represents a unique player
        :return: the player's fish count, an int
        """
        return self.__player_fish_count[player_id]

    def skip_turn(self, player_id):
        """
        int -> bool
        If there are no moves for a player to make, then the turn should be skipped. Public for referees to use.
        :param player_id: an int that represents a unique player
        :return: True if the turn was skipped and False if not
        """
        if not self.get_all_reachable_dests(player_id):
            self.__update_turns()
            return True
        return False

    def __update_turns(self):
        """
        Nothing (uses class variables) -> Nothing (Void function)
        This method updates whose turn it is. The "first" element of the player_order variable is the
        player whose turn it is. This update_turns is called when a player has finished taking their
        turn. Therefore, I just do a cyclic shift by adding that player to the end of the list.
        """
        player_who_took_a_turn = self.__player_order.pop(0)
        self.__player_order.append(player_who_took_a_turn)

    def place_avatar(self, player_id, desired_posn):
        """
        int [int, int] -> bool
        The purpose of this function is to execute the pre-gameplay 'placement phase'. Meaning, before the
        game has started, players need to place their penguins on initial spots. This function should not
        be used to move a penguin from an existing posn to another posn.
        :param player_id: an int that represents a unique player
        :param desired_posn: a List of the form [row, col] where row and col are both ints, representing the
        posn that the player wants to move to
        :return True if the avatar was able to be placed (passed the checks and placement phase was not over) and
        False if not (either did not pass the checks or the placement phase was over)...these are
        messages for the referee
        """
        # These checks can later be moved to referee functionality
        # The check self.__player_order[0] == player_id asserts that it is this players' turn

        if not self.is_pos_out_of_bounds(desired_posn) and self.is_unoccupied(desired_posn) and \
                not self.is_hole(desired_posn) and self.__player_order[0] == player_id:
            player_penguin_posns = self.__penguin_posns[player_id]
            for i, current_pos in enumerate(player_penguin_posns):
                # That means the placement phase is still ongoing for this player
                if not current_pos:
                    player_penguin_posns[i] = desired_posn
                    self.__penguin_posns[player_id] = player_penguin_posns
                    self.__update_turns()
                    return True
        return False

    def __update_player_fish_count(self, player_id, start_posn):
        """
        int [int, int] -> Nothing (Void function)
        The purpose of this function is to update the player fish count if they have placed their avatar on a tile/
        moved to a tile. I am making it private because this method is going to be called by the placement/move
        methods and should not be called directly by the referee or the players.
        :param player_id:  an int that represents a unique player
        :param start_posn: a List of the form [row, col] where row and col are both ints, representing the
        posn that the player wants to move to
        """
        board_tiles = self.__board.get_tiles()

        start_posn_row = start_posn[0]
        start_posn_col = start_posn[1]
        tile_at_pos = board_tiles[start_posn_row][start_posn_col]
        tile_fish_count = tile_at_pos.get_num_fish_per_tile()
        self.__player_fish_count[player_id] += tile_fish_count

    def is_placement_phase_over(self):
        """
        Nothing (uses class variables) -> bool
        Determines whether the placement phase is over for the game.
        :return: True if the placement phase is over and False if not
        """
        for player_id in self.__penguin_posns:
            for posn in self.__penguin_posns[player_id]:
                if not posn:
                    return False
        return True

    def move_avatar(self, player_id, start_posn, desired_posn):
        """
        int [int, int] [int, int] -> bool
        The purpose of this function is to move a player's avatar from an existing posn to
        another posn, when the game is ongoing. This can only be done if the player exists,
        if the player has an avatar at the original posn, if the desired posn is
        on the board and is not occupied by another avatar, and if the desired posn is
        reachable from the original posn. Player id will be error-checked since referee
        will be calling this function and referee should be giving valid inputs.
        :param player_id: an int that represents a unique player
        :param start_posn: a List of the form [row, col] where row and col are both ints, representing the
        posn that the player wants to move from
        :param desired_posn:a List of the form [row, col] where row and col are both ints, representing the
        posn that the player wants to move to
        :return True if the move happened (passed the checks) and
        False if not (did not pass the checks)...these are messages for the referee
        """
        # These checks can later be moved to referee functionality
        # The check self.__player_order[0] == player_id asserts that it is this players' turn
        if not self.is_pos_out_of_bounds(desired_posn) and \
                self.is_unoccupied(desired_posn) and \
                self.player_has_penguin_at_pos(player_id, start_posn) and \
                desired_posn in self.get_all_reachable_dests(player_id) and \
                self.__player_order[0] == player_id:

            player_penguin_posns = self.__penguin_posns[player_id]

            original_posn_index = player_penguin_posns.index(start_posn)
            player_penguin_posns[original_posn_index] = desired_posn
            self.__penguin_posns[player_id] = player_penguin_posns

            self.__update_player_fish_count(player_id, start_posn)

            self.__board.remove_tile(start_posn)

            self.__update_turns()
            return True

        return False

    def player_can_make_move(self, player_id):
        """
        int -> bool
        Determines whether a player still has moves left. This means that
        for a player, and for some avatar it has, there is at least one unoccupied and reachable tile that the
        avatar can potentially move to. Or the placement phase is still going on for that player.
        I am making this public in case referees or players want to use it for rule-checking.
        :param player_id: an int that represents a unique player
        :return: True if there are still moves left for the player and False if not
        """
        player_penguin_posns = self.__penguin_posns[player_id]
        for posn in player_penguin_posns:
            # placement phase is still going on, so there are still empty lists
            if not posn:
                return True
            else:
                reachable_posns = self.__board.get_reachable_posns(posn, player_penguin_posns)
                if len(reachable_posns) > 0:
                    for reachable_posn in reachable_posns:
                        if self.is_unoccupied(reachable_posn):
                            return True
        return False

    def is_game_over(self):
        """
        Nothing (uses class variables) -> bool
        The purpose of this function is to determine whether any player can move an avatar. This means that
        for some player, and for some avatar it has, there is at least one unoccupied and reachable tile that the
        avatar can potentially move to. Or the placement phase is still going on for that player.
        :return: False if there are moves left (above conditions are fulfilled) and True if not
        """
        for player_id in self.__penguin_posns:
            if self.player_can_make_move(player_id):
                return False
        return True

    def render_game_state(self):
        """
        Nothing (uses class variables) -> Nothing
        Function to draw the game state (the game board with tiles and fish, and penguins on it). 
        A tile that is invisible still has its outline drawn for a better user experience.
        We determine x and y posns of the tiles based on the dimensions of a tile and give offsets 
        depending on the row and col and whether they are even or odd values.
        """
        root = tkinter.Tk()
        canvas_height = self.__board.get_rows() * TILE_SIZE + 2 * TILE_SIZE
        canvas_width = self.__board.get_columns() * 5 * TILE_SIZE
        canvas = tkinter.Canvas(root, bg="white", width=canvas_width, height=canvas_height)

        board_tiles = self.__board.get_tiles()
        for i in range(len(board_tiles)):
            for j in range(len(board_tiles[i])):
                tile = board_tiles[i][j]

                fish_count = tile.get_num_fish_per_tile()
                # draw a tile
                if i % 2 == 0:
                    x1 = TILE_SIZE + TILE_X_OFFSET + j * (3 * TILE_SIZE) + j * TILE_SIZE
                    y1 = TILE_Y_OFFSET + (i // 2) * 2 * TILE_SIZE
                else:
                    x1 = 3 * TILE_SIZE + TILE_X_OFFSET + \
                         j * (3 * TILE_SIZE) + j * TILE_SIZE
                    y1 = TILE_Y_OFFSET + TILE_SIZE + (i // 2) * 2 * TILE_SIZE

                sequence = [x1, y1,
                            (x1 - TILE_SIZE), y1 + TILE_SIZE,
                            x1, y1 + (2 * TILE_SIZE),
                            x1 - TILE_SIZE + (2 * TILE_SIZE), y1 + (2 * TILE_SIZE),
                            (x1 - TILE_SIZE) + 3 * TILE_SIZE, y1 + TILE_SIZE,
                            (x1 - TILE_SIZE) + 2 * TILE_SIZE, y1]

                if not tile.get_visibility():
                    canvas.create_polygon(sequence, outline='black', fill='')

                else:
                    canvas.create_polygon(sequence, outline='black', fill='orange')
                    penguin_on_tile = False
                    for player_id in self.__penguin_posns:
                        if self.player_has_penguin_at_pos(player_id, [i, j]):
                            player_penguin_color = self.__player_penguin_colors[player_id]
                            penguin = penguin_inst(x1, y1, player_penguin_color)
                            penguin.draw_penguin(canvas)
                            penguin_on_tile = True
                            break
                    if not penguin_on_tile:
                        for y in range(fish_count):
                            fish = fish_inst(x1, y1)
                            fish.draw_fish(canvas, y)

        canvas.pack()
        root.mainloop()

    def get_board(self):
        """
        Getter method for the board private variable.
        :return: self.__board, a Board object
        """
        return self.__board

    def get_player_penguin_colors(self):
        """
        Getter method for the player_penguin_colors private variable. {player_id: player_penguin_color}, where a
        player_id is an int and a player_penguin_color is a String
        :return: self.__player_penguin_colors
        """
        return self.__player_penguin_colors

    def get_player_order(self):
        """
        Getter method for the player_order private variable. Useful for referee.
        :return: self.__player_order, of the form [player_id], where player_id is an int
        """
        return self.__player_order

    def get_player_fish_count(self):
        """
        Getter method for the player_fish_count private variable. Useful for players to see if they are winning
        or losing.
        :return: self.__player_fish_count, {player_id: fish_count}
        """
        return self.__player_fish_count

    def get_penguin_posns(self):
        """
        Getter method for the penguin_posns private variable. Useful for players to make strategic decisions
        and for the referee to rule check.
        :return: self.__penguin_posns, {player_id: [[row,col]]}
        """
        return self.__penguin_posns
