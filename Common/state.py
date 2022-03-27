from fish import __Fish as fish_inst
from penguin import __Penguin as penguin_inst
from tile_fish_penguin_constants import TILE_SIZE
import tkinter

"""
This class essentially can tell you what the state of a game is, giving you a snapshot of the game at a particular 
moment in time. This includes things like the state of the board (what tiles are on the board, where the holes are 
on the board, how many fish are on a tile, etc) and things like the player penguin colors, the order in which 
players play, whose turn it currently is, how many fish each player has, and where each player's penguins are located.
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
        penguin_posns = {}
        num_of_players = len(self.__player_penguin_colors)
        penguins_per_player = 6 - num_of_players

        for player_id in self.__player_penguin_colors:
            penguin_posns[player_id] = [[] for _i in range(penguins_per_player)]

        self.__penguin_posns = penguin_posns

    def is_pos_out_of_bounds(self, posn):
        board_rows = self.__board.get_rows()
        board_columns = self.__board.get_columns()

        pos_row = posn[0]
        pos_col = posn[1]

        return (pos_row < 0 or pos_row >= board_rows) or (pos_col < 0 or pos_col >= board_columns)

    def player_has_penguin_at_pos(self, player_id, posn):
        player_penguin_posns = self.__penguin_posns[player_id]
        return posn in player_penguin_posns

    def is_hole(self, posn):
        board_tiles = self.__board.get_tiles()
        pos_row = posn[0]
        pos_col = posn[1]
        tile_at_pos = board_tiles[pos_row][pos_col]

        return not tile_at_pos.get_visibility()

    def is_unoccupied(self, posn):
        for player_id in self.__penguin_posns:
            if self.player_has_penguin_at_pos(player_id, posn):
                return False
        return True

    def get_all_reachable_dests_help(self, start_pos, lo_all_penguin_posns, recurse):
        all_destinations = []
        destinations = self.__board.get_reachable_posns(start_pos, lo_all_penguin_posns, recurse)
        for dest_pos in destinations:
            if dest_pos not in all_destinations and self.is_unoccupied(dest_pos):
                all_destinations.append(dest_pos)
        return all_destinations

    def get_all_reachable_dests(self, player_id, which_penguin=None, recurse=True):
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
        self.__player_penguin_colors.pop(player_id)
        self.__player_order.remove(player_id)
        self.__player_fish_count.pop(player_id)
        self.__penguin_posns.pop(player_id)

    def get_winning_score(self):
        return max(self.__player_fish_count.values())

    def get_player_score(self, player_id):
        return self.__player_fish_count[player_id]

    def skip_turn(self, player_id):
        if not self.get_all_reachable_dests(player_id):
            self.__update_turns()
            return True
        return False

    def __update_turns(self):
        player_who_took_a_turn = self.__player_order.pop(0)
        self.__player_order.append(player_who_took_a_turn)

    def place_avatar(self, player_id, desired_posn):
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
        board_tiles = self.__board.get_tiles()

        start_posn_row = start_posn[0]
        start_posn_col = start_posn[1]
        tile_at_pos = board_tiles[start_posn_row][start_posn_col]
        tile_fish_count = tile_at_pos.get_num_fish_per_tile()
        self.__player_fish_count[player_id] += tile_fish_count

    def is_placement_phase_over(self):
        for player_id in self.__penguin_posns:
            for posn in self.__penguin_posns[player_id]:
                if not posn:
                    return False
        return True

    def move_avatar(self, player_id, start_posn, desired_posn):
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
        for player_id in self.__penguin_posns:
            if self.player_can_make_move(player_id):
                return False
        return True

    def render_game_state(self):
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
        return self.__board

    def get_player_penguin_colors(self):
        return self.__player_penguin_colors

    def get_player_order(self):
        return self.__player_order

    def get_player_fish_count(self):
        return self.__player_fish_count

    def get_penguin_posns(self):
        return self.__penguin_posns
