from tile_fish_penguin_constants import FISH_SIZE


class __Fish:
    """
    This class represents a Fish image. 

    This is a private class, as I don't want the user to have direct access to it. Functionality (which includes error
    checking x and y) is done through board methods.
    :param x: the x coordinate of the fish
    :param y: the y coordinate of the fish
    """
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    # create one little triangle + one little circle next to it = fish image
    def draw_fish(self, canvas, placement_offset):
        """
        Draws the fish on the canvas, which is passed in from board. Placement_offset: dictates whether you are the 
        1st, 2nd, 3rd...etc fish to be placed. So I move down based on what number fish you are.
        """
        #  hor_ver_offset basically dictates the offset to create the bounding box for when we draw the
        #  triangle and circle.
        hor_ver_offset = (FISH_SIZE // 2) - 1
        # little triangle
        sequence = [self.__x, self.__y + placement_offset * (FISH_SIZE + hor_ver_offset),
                    self.__x, self.__y + placement_offset * (FISH_SIZE + hor_ver_offset) + FISH_SIZE,
                    self.__x + hor_ver_offset, self.__y + placement_offset * (FISH_SIZE + hor_ver_offset) + hor_ver_offset]
        canvas.create_polygon(sequence, fill='blue')
        # little circle
        canvas.create_oval(self.__x + hor_ver_offset, self.__y + placement_offset * (FISH_SIZE + hor_ver_offset),
                            self.__x + 2 * FISH_SIZE, self.__y + placement_offset * (FISH_SIZE + hor_ver_offset) + FISH_SIZE, fill='blue')

