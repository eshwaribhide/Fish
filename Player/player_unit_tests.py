import unittest
import sys
from player import Player
sys.path.append('../Common')
from board import Board
from state import GameState


class TestPlayer(unittest.TestCase):

    def test_place_avatar(self):
        board = Board(2, 5, {0: [0, 1]}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [1, 2],
                          penguin_posns={1: [[0, 0], [0, 1], [], []], 2: [[1, 0], [1, 1], [], []]})
        player1 = Player(1)
        player2 = Player(2)
        assert player1.place_avatar(state) == [0, 2]
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], []], 2: [[1, 0], [1, 1], [], []]})
        assert player2.place_avatar(state) == [0, 3]


    def test_move_avatar(self):
        board = Board(2, 5, {}, num_of_fish_per_tile=2)

        state = GameState(board, {1: "black", 2: "white"}, [1, 2],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        player1 = Player(1)
        player2 = Player(2)
        assert player1.move_avatar(state) == ((1,3), (0, 3))

        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        assert player2.move_avatar(state) == ((1, 2), (0, 3))


if __name__ == '__main__':
    unittest.main()