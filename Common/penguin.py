from tile_fish_penguin_constants import FISH_SIZE, PENGUIN_SIZE


class __Penguin:
    """
    This class represents a Penguin avatar. It is passed in the args, x & y, which represents the x & y coordinates of the penguin.
    It also passes in the args color, which represents the color of the penguin.
    The color will be set to only the penguin colors defined in Constants, when a penguin instance is created.
    This is a private class, as we don't want the user to have direct access to it. Functionality will be done
    through board methods; this is why we don't error check x and y because that will be done in the board methods.
    :param x: the x coordinate of the penguin
    :param y: the y coordinate of the penguin
    :param color: the color of the penguin
     """
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__color = color

    # we create one little circle + one oval below it = penguin image
    def draw_penguin(self, canvas):
        """
        Draws the penguin on the canvas.
        :param canvas: The canvas is passed in through the board.
        """
        # little circle
        canvas.create_oval(self.__x + FISH_SIZE//2, self.__y, self.__x + PENGUIN_SIZE, self.__y+FISH_SIZE, fill=f'{self.__color}')
        # oval below it
        canvas.create_oval(self.__x + FISH_SIZE//2, self.__y + FISH_SIZE, self.__x + PENGUIN_SIZE, self.__y+2*PENGUIN_SIZE, fill=f'{self.__color}')



