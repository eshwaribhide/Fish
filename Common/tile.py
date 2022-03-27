class __Tile:
    """
    This class represents a Tile on the board.

    This is a private class, as I don't want the user to have direct access to it. Functionality in terms of
    rendering is done through board methods.
    """
    def __init__(self, num_fish_per_tile):
        self.__num_fish_per_tile = num_fish_per_tile
        self.__is_visible = True

    def get_num_fish_per_tile(self):
        return self.__num_fish_per_tile

    def get_visibility(self):
        return self.__is_visible

    def set_invisible(self):
        self.__is_visible = False

