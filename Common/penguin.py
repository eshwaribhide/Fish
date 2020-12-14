from tile_fish_penguin_constants import FISH_SIZE, PENGUIN_SIZE


class __Penguin:
    """
    This class represents a Penguin avatar. 
    The color will be set to only the penguin colors defined in Constants, when a penguin instance is created.
    This is a private class, as I don't want the user to have direct access to it. Functionality (including error checking x and y) will be done
    through board methods.
    :param x: the x coordinate of the penguin
    :param y: the y coordinate of the penguin
    :param color: the color of the penguin
     """
    def __init__(self, x, y, color):
        self.__x = x
        self.__y = y
        self.__color = color

    # I create one little circle + one oval below it = penguin image
    def draw_penguin(self, canvas):
        """
        Draws the penguin on the canvas.
        """
        # little circle
        canvas.create_oval(self.__x + FISH_SIZE//2, self.__y, self.__x + PENGUIN_SIZE, self.__y+FISH_SIZE, fill=f'{self.__color}')
        # oval below it
        canvas.create_oval(self.__x + FISH_SIZE//2, self.__y + FISH_SIZE, self.__x + PENGUIN_SIZE, self.__y+2*PENGUIN_SIZE, fill=f'{self.__color}')



