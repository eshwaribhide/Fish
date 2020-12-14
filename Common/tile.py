class __Tile:
    """
    This class represents a Tile on the board.

    This is a private class, as I don't want the user to have direct access to it. Functionality in terms of
    rendering is done through board methods.
    """
    def __init__(self, num_fish_per_tile):
        self.__num_fish_per_tile = num_fish_per_tile
        self.__is_visible = True  # True if the tile is visible, False if it is not (it has been removed)

    def get_num_fish_per_tile(self):
        """
        :returns num_fish_per_tile: the amount of fish on the tile
        """
        return self.__num_fish_per_tile

    def get_visibility(self):
        """
        :returns visibility: True if the tile is visible, False if it has been removed
        """
        return self.__is_visible

    def set_invisible(self):
        """
        Sets the tile to being invisible (is_visible is False) to represent a removed tile
        """
        self.__is_visible = False

