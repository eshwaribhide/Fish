from tile import __Tile as tile_inst
from tile_fish_penguin_constants import MAX_FISH
import random

"""
holes is of the form {row : [columns]}
tiles is of the form [[row, col]]

Coordinate System of [row, col]. They are 0-indexed. So [0,0] represents the leftmost, topmost position on the board, [0,1]
is the position directly to the right but in the same row as [0,0]. [1,0] is the position directly below but in the same
column as [0,0], and these values also correspond to the indexes in self.__tiles, which can be used to find
the corresponding tile at the position. So if you want to find the tile located at [0,0] in the board, do self.__tiles[0][0].

A BOARD IS COMPOSED OF TILES (DOUBLE-NESTED ARRAY OF TILE OBJECTS, SEE BELOW FOR MORE INFO RIGHT ABOVE SELF.__TILES).
A BOARD HAS A SET NUMBER OF ROWS AND COLUMNS (BOTH ARE INTS). A BOARD ALSO HAS THE POTENTIAL TO HAVE HOLES. A HOLE IS A TILE
THAT HAS ITS VISIBILITY SET TO FALSE. IN A REAL BOARD, IT WOULD BE AN EMPTY SPOT. A BOARD DOES NOT HAVE TO HAVE HOLES. 
A BOARD HAS THE POTENTIAL TO HAVE A MINIMUM NUMBER OF ONE-FISH TILES AND A NUMBER OF FISH PER TILE (BOTH INTS), BUT DOES NOT HAVE TO.
SO, A BOARD IS A CLASS WITH CERTAIN VARIABLES REPRESENTING ALL THESE THINGS. PLEASE SEE THE IMPLEMENTATION
OF THE CLASS BELOW FOR MORE SPECIFICS.
"""


class Board:
    """
    This class represents the data representation of a Board. It is passed in the args,row,columns,holes,min_num_one_fish_tiles,
    num_of_fish_per_tile, which represents the qualities of the board. It contains static functions to
    check the args. See DATA DEFINITION OF TILES BELOW (right above declaration of tiles class variable).
    :param rows: the amount of rows, an int
    :param columns: the amount of columns, an int
    :param holes: the posns of the holes, a dict {row : [columns]} where the rows & columns represent the posns of
    empty tiles, we chose to use a dictionary to use less space than a double-nested array of [[row, col]]
    :param min_num_one_fish_tiles: 0 predetermined, otherwise an int that the user specifies
    :param num_of_fish_per_tile: None predetermined, otherwise an int that the user specifies
    # num of fish per tile is initialized to None because there is a potential that it is unspecified
    # we don't want to confuse it with 0, so the possible types are None (unspecified) or some val
    # >= 1.

    See DATA DEFINITION OF TILES BELOW (right above declaration of tiles class variable).
    AND SEE ABOVE FOR THE DATA TYPES OF EACH VARIABLE!!!
    """

    def __init__(self, rows, columns, holes, min_num_one_fish_tiles=0, num_of_fish_per_tile=None):
        self.__error_check_rows_and_columns(rows, columns)
        self.__error_check_holes(holes)
        self.__error_check_min_num_one_fish_tiles(min_num_one_fish_tiles, (rows * columns))
        self.__error_check_num_of_fish_per_tile(num_of_fish_per_tile)
        self.__check_conflict_fish_per_tile(min_num_one_fish_tiles, num_of_fish_per_tile)

        self.__rows = rows
        self.__columns = columns
        self.__holes = holes
        self.__min_num_one_fish_tiles = min_num_one_fish_tiles

        # this value is error checked in Tile, since it depends on the max # of fish of which the
        # tile class has control
        self.__num_of_fish_per_tile = num_of_fish_per_tile

        # Data description: a 2D array where the length of the array is the # of rows, and the length of each nested
        # array is the number of columns. It’s indexed by row-col ([0][1] is row 0 column 1). In each nested array
        # is a Tile object.
        self.__tiles = []

        self.__initialize_game_board()

    # static method because it has nothing to do with modifying the class state
    @staticmethod
    def __error_check_rows_and_columns(rows, columns):
        """
       Checks if rows and columns are valid args.
       :param rows: the amount of rows
       :param columns: the amount of columns
        """
        if not isinstance(rows, int) or not isinstance(columns, int):
            raise TypeError('Rows and columns must both be of integer type')
        if rows < 1 or columns < 1:
            raise ValueError('There must be at least 1 row and column')

    @staticmethod
    def __error_check_holes(holes):
        """
        Checks if holes is a valid arg
        :param holes: a dict {row : [columns]} representing the hole posns
        """
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
        """
        Checks if min_num_one_fish_tiles is valid arg
        :param min_num_one_fish_tiles: the minimum amount of single fish tiles
        :param max_tiles: the max amount of tiles that can be on the board
        """
        if not isinstance(min_num_one_fish_tiles, int):
            raise TypeError('Min num one fish tiles must be an int')
        if min_num_one_fish_tiles > max_tiles or min_num_one_fish_tiles < 0:
            raise ValueError(f'Min num one fish tiles (x) must be 0 <= x <= {max_tiles}')

    @staticmethod
    def __error_check_num_of_fish_per_tile(num_of_fish_per_tile):
        """
       Checks if num_of_fish_per_tile is a valid arg
       :param num_of_fish_per_tile: the amount of fish per tile
       """
        if num_of_fish_per_tile is not None:
            if not isinstance(num_of_fish_per_tile, int):
                raise TypeError('Num of fish per tile must be either None or an int')
            if num_of_fish_per_tile > MAX_FISH or num_of_fish_per_tile < 1:
                raise ValueError(f'Num of fish per tile (x) must be 1 <= x <= {MAX_FISH}')

    @staticmethod
    def __check_conflict_fish_per_tile(min_num_one_fish_tiles, num_of_fish_per_tile):
        """
        Checks if these two values conflict. They cannot both be non-null and greater than 0 at the same time.
        :param min_num_one_fish_tiles: the minimum amount of single fish tiles
        :param num_of_fish_per_tile: the amount of fish per tile
        """
        if num_of_fish_per_tile is not None and num_of_fish_per_tile > 1 and min_num_one_fish_tiles > 0:
            raise ValueError('Cannot have a minimum number of one fish tiles alongside a specified num fish per tile')

    def __initialize_game_board(self):
        """
        Initializes the board. It takes into consideration different aspects such as whether to add
        holes, where those holes are, the minimum number of one fish tiles, and the number of fish
        per tile.
        """
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
        """
        [int, int] -> bool
        Checks if the selected tile is empty
        :param posn a List of the form [row, col] where row and col are both ints
        :returns True if the tile is invisible and False if it is visible
        """
        tile_row = posn[0]
        tile_col = posn[1]
        tile = self.__tiles[tile_row][tile_col]
        tile_visibility = tile.get_visibility()
        return not tile_visibility

    def __check_pos_out_of_bounds(self, posn):
        """
        [int, int] -> bool
        Checks if the selected tile posn is out of bounds
        :param posn: an list representing row as first val and col as second val
        :returns True if either the row or col val is out of bounds and false if not
        """
        pos_row = posn[0]
        pos_col = posn[1]

        if pos_row >= 0 and pos_col >= 0:
            return pos_row >= self.__rows or pos_col >= self.__columns
        return True

    def __get_reachable_posns_help(self, start_posn, pos_acc, lo_all_penguin_posns, recurse, **kwargs):
        """
         [int, int] [[int, int]] [[int, int]] bool {str:int, str:int, str:int, str:int} -> [[int, int]]
        Helper function to find reachable posns of a tile.There is a flag called recurse. This was added due
        to the integration tests. If you only want to see the reachable posns that are one step
        away, then recurse will be set to False. If you want to see all the reachable posns, then
        recurse is True.
        :param start_posn a List of the form [row, col] where row and col are both ints that we
        are calculating reachable posns relative to
        :param pos_acc:  list of all of the reachable posns
        :param lo_all_penguin_posns: a List of the form [row] col where row and col are both ints, representing
        posns on which penguins are resting, so as to not deem them reachable.
        :param recurse Will be true if recursion should be done at the end of the method, and False if not
        :param **kwargs: keyword args, essentially a dictionary that contains even/odd row/col shifts
        looks like {"even_row_shift":int, "odd_row_shift":int, "even_col_shift":int, "odd_col_shift":int}
        :return pos_acc, the list of all the reachable posns, a [[row,col]]
        """
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
        """
        [int, int] [[int, int]] bool -> [[int, int]]
        Function to find reachable posns of a tile. There are six directions that define reachability,
        which are north, northwest, southwest, south, southeast, and northeast. This function will get
        all the posns that are reachable in all the different directions and then tack them on to
        reachable_posns, which is the return. There is a flag called recurse. This was added due
        to the integration tests. If you only want to see the reachable posns that are one step
        away, then recurse will be set to False. If you want to see all the reachable posns, then
        recurse is True.
        :param start_posn a List of the form [row, col] where row and col are both ints that we
        are calculating reachable posns relative to
        :param lo_all_penguin_posns a List of the form [row] col where row and col are both ints, representing
        posns on which penguins are resting, so as to not deem them reachable.
        :param recurse Set to true if recursion should be done in the helper method, and False if not
        :return a double-nested array containing all the posns that are reachable
        """
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
        """
        int int -> no return (void function)
        Function remove a tile by setting it to be invisible (representing removed tile).
        :param posn: a List of the form [row, col] where row and col are both ints
        """
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
        """
        Getter method for rows private variable.
        :return: self.__rows, an int
        """
        return self.__rows

    def get_columns(self):
        """
        Getter method for columns private variable.
        :return: self.__columns, an int
        """
        return self.__columns

    def get_holes(self):
        """
        Getter method for holes private variable.
        :return: self.__holes, a Dict {row:[col vals]}
        """
        return self.__holes

    def get_min_num_one_fish_tiles(self):
        """
        Getter method for min num one fish tiles private variable.
        :return: self.__min_num_one_fish_tiles, an int
        """
        return self.__min_num_one_fish_tiles

    def get_num_of_fish_per_tile(self):
        """
        Getter method for num of fish per tile private variable.
        :return: self.__num_of_fish_per_tile, an int
        """
        return self.__num_of_fish_per_tile

    def get_tiles(self):
        """
        Getter method for tiles private variable.
        :return: self.__tiles a [[Tile]]
        """
        return self.__tiles
