from tile import __Tile as tile_inst
from tile_fish_penguin_constants import MAX_FISH
import random

"""
A board is composed of tiles. A board has a set number of rows and columns (both are ints). A board also has the 
potential to have holes. A hole is a tile that has its visibility set to false. In a real board, it would be an empty 
spot. A board does not have to have holes. A board has the potential to have a minimum number of one-fish tiles and a 
number of fish per tile (both ints), but does not have to.

A board uses the coordinate system of [row, col], 0-indexed. So [0,0] represents the leftmost, topmost position on the 
board, [0,1] is the position directly to the right but in the same row as [0,0]. [1,0] is the position directly below 
but in the same column as [0,0], and these values also correspond to the indexes in self.__tiles, which can be used to 
find the corresponding tile at the position.
"""


class Board:
    
    def __init__(self, rows, columns, holes, min_num_one_fish_tiles=0, num_of_fish_per_tile=None):
        self.__error_check_rows_and_columns(rows, columns)
        self.__error_check_holes(holes)
        self.__error_check_min_num_one_fish_tiles(min_num_one_fish_tiles, (rows * columns))
        self.__error_check_num_of_fish_per_tile(num_of_fish_per_tile)
        self.__check_conflict_fish_per_tile(min_num_one_fish_tiles, num_of_fish_per_tile)

        self.__rows = rows
        self.__columns = columns
        # a dict {row : [columns]} where a key-val pair is a posn of a hole on the board
        self.__holes = holes
        self.__min_num_one_fish_tiles = min_num_one_fish_tiles

        # this value is error checked in Tile, since it depends on the max # of fish of which the
        # tile class has control
        # Also, it is initialized to None because there is a potential that it is unspecified
        # I don't want to confuse it with 0, so the possible types are None (unspecified) or some val
        # >= 1.
        self.__num_of_fish_per_tile = num_of_fish_per_tile

        # Data description: a 2D array where the length of the array is the # of rows, and the length of each nested
        # array is the number of columns. It’s indexed by row-col ([0][1] is row 0 column 1). In each nested array
        # is a Tile object.
        self.__tiles = []

        self.__initialize_game_board()

    @staticmethod
    def __error_check_rows_and_columns(rows, columns):
        if not isinstance(rows, int) or not isinstance(columns, int):
            raise TypeError('Rows and columns must both be of integer type')
        if rows < 1 or columns < 1:
            raise ValueError('There must be at least 1 row and column')

    @staticmethod
    def __error_check_holes(holes):
        if not isinstance(holes, dict):
            raise TypeError('Holes must be a dictionary')
        for i in holes:
            if not isinstance(i, int):
                raise TypeError('Holes must be a dictionary of {int: [int, int]}')
            if not isinstance(holes[i], list):
                raise TypeError('Holes must be a dictionary of {int: [[int, int]]}')
            for j in holes[i]:
                if not isinstance(j, int):
                    raise TypeError('Holes must be a dictionary of {int: [[int, int]]}')

    @staticmethod
    def __error_check_min_num_one_fish_tiles(min_num_one_fish_tiles, max_tiles):
        if not isinstance(min_num_one_fish_tiles, int):
            raise TypeError('Min num one fish tiles must be an int')
        if min_num_one_fish_tiles > max_tiles or min_num_one_fish_tiles < 0:
            raise ValueError(f'Min num one fish tiles (x) must be 0 <= x <= {max_tiles}')

    @staticmethod
    def __error_check_num_of_fish_per_tile(num_of_fish_per_tile):
        if num_of_fish_per_tile is not None:
            if not isinstance(num_of_fish_per_tile, int):
                raise TypeError('Num of fish per tile must be either None or an int')
            if num_of_fish_per_tile > MAX_FISH or num_of_fish_per_tile < 1:
                raise ValueError(f'Num of fish per tile (x) must be 1 <= x <= {MAX_FISH}')

    @staticmethod
    def __check_conflict_fish_per_tile(min_num_one_fish_tiles, num_of_fish_per_tile):
        if num_of_fish_per_tile is not None and num_of_fish_per_tile > 1 and min_num_one_fish_tiles > 0:
            raise ValueError('Cannot have a minimum number of one fish tiles alongside a specified num fish per tile')

    def __initialize_game_board(self):
        num_one_fish_tiles_left_to_add = self.__min_num_one_fish_tiles
        tiles_per_row = []
        for i in range(self.__rows):
            tiles_per_column = []
            for j in range(self.__columns):
                if num_one_fish_tiles_left_to_add > 0:
                    tiles_per_column.append(tile_inst(1))
                    num_one_fish_tiles_left_to_add -= 1
                else:
                    tile_fish_count = self.__num_of_fish_per_tile if self.__num_of_fish_per_tile \
                                                                     is not None else random.randint(1, MAX_FISH)
                    tile = tile_inst(tile_fish_count)
                    if i in self.__holes and j in self.__holes[i]:
                        tile.set_invisible()
                    tiles_per_column.append(tile)
            tiles_per_row.append(tiles_per_column)
        self.__tiles = tiles_per_row

    def __check_empty_tile(self, posn):
        tile_row = posn[0]
        tile_col = posn[1]
        tile = self.__tiles[tile_row][tile_col]
        tile_visibility = tile.get_visibility()
        return not tile_visibility

    def __check_pos_out_of_bounds(self, posn):
        pos_row = posn[0]
        pos_col = posn[1]

        if pos_row >= 0 and pos_col >= 0:
            return pos_row >= self.__rows or pos_col >= self.__columns
        return True

    def __get_reachable_posns_help(self, start_posn, pos_acc, lo_all_penguin_posns, recurse, **kwargs):
        tile_row = start_posn[0]
        tile_column = start_posn[1]

        even_row_shift = kwargs["even_row_shift"]
        odd_row_shift = kwargs["odd_row_shift"]

        even_col_shift = kwargs["even_col_shift"]
        odd_col_shift = kwargs["odd_col_shift"]

        new_row = tile_row + even_row_shift if tile_row % 2 == 0 else tile_row + odd_row_shift
        new_col = tile_column + even_col_shift if tile_row % 2 == 0 else tile_column + odd_col_shift

        new_posn = [new_row, new_col]

        if self.__check_pos_out_of_bounds(new_posn):
            return pos_acc

        if self.__check_empty_tile(start_posn) or self.__check_empty_tile(new_posn):
            return pos_acc

        if new_posn in lo_all_penguin_posns:
            return pos_acc

        pos_acc.append(new_posn)

        if recurse:
            return self.__get_reachable_posns_help(new_posn, pos_acc, lo_all_penguin_posns, recurse, **kwargs)
        else:
            return pos_acc

    def get_reachable_posns(self, start_posn, lo_all_penguin_posns, recurse=True):
        if self.__check_pos_out_of_bounds(start_posn):
            raise ValueError('Row must be 1 <= x < self.rows, column must be 1 <=x < self.columns')

        if self.__check_empty_tile(start_posn):
            raise ValueError('Nowhere reachable from an empty tile')

        reachable_posns = []

        # north
        reachable_posns.extend(self.__get_reachable_posns_help(start_posn, [],
                                                                       lo_all_penguin_posns,
                                                                       recurse,
                                                                       even_row_shift=-2, odd_row_shift=-2,
                                                                       even_col_shift=0, odd_col_shift=0))

        # northeast
        reachable_posns.extend(self.__get_reachable_posns_help(start_posn, [],
                                                                       lo_all_penguin_posns,
                                                                       recurse,
                                                                       even_row_shift=-1, odd_row_shift=-1,
                                                                       even_col_shift=0, odd_col_shift=1))

        # southeast
        reachable_posns.extend(self.__get_reachable_posns_help(start_posn, [],
                                                                       lo_all_penguin_posns,
                                                                       recurse,
                                                                       even_row_shift=1, odd_row_shift=1,
                                                                       even_col_shift=0, odd_col_shift=1))
        # south
        reachable_posns.extend(self.__get_reachable_posns_help(start_posn, [],
                                                                       lo_all_penguin_posns,
                                                                       recurse,
                                                                       even_row_shift=2, odd_row_shift=2,
                                                                       even_col_shift=0, odd_col_shift=0))

        # southwest
        reachable_posns.extend(self.__get_reachable_posns_help(start_posn, [],
                                                                       lo_all_penguin_posns,
                                                                       recurse,
                                                                       even_row_shift=1, odd_row_shift=1,
                                                                       even_col_shift=-1, odd_col_shift=0))

        # northwest
        reachable_posns.extend(self.__get_reachable_posns_help(start_posn, [],
                                                                       lo_all_penguin_posns,
                                                                       recurse,
                                                                       even_row_shift=-1, odd_row_shift=-1,
                                                                       even_col_shift=-1, odd_col_shift=0))

        return reachable_posns

    def remove_tile(self, posn):
        if self.__check_pos_out_of_bounds(posn):
            raise ValueError('Row must be 1 <= x < self.rows, column must be 1 <=x < self.columns')

        if self.__check_empty_tile(posn):
            raise ValueError('Tile has already been removed')

        tile_row = posn[0]
        tile_column = posn[1]

        tile_to_change = self.__tiles[tile_row][tile_column]
        tile_to_change.set_invisible()

        if tile_row in self.__holes:
            self.__holes[tile_row].append(tile_column)
        else:
            self.__holes[tile_row] = [tile_column]

    def get_rows(self):
        return self.__rows

    def get_columns(self):
        return self.__columns

    def get_holes(self):
        return self.__holes

    def get_min_num_one_fish_tiles(self):
        return self.__min_num_one_fish_tiles

    def get_num_of_fish_per_tile(self):
        return self.__num_of_fish_per_tile

    def get_tiles(self):
        return self.__tiles
