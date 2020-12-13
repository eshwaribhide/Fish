import unittest
import sys
from strategy import Strategy
sys.path.append('../Common')
from board import Board
from state import GameState
from tile import __Tile as tile_inst


class TestStrategy(unittest.TestCase):

    def test_zig_zag(self):
        board = Board(2, 5, {0: [0, 1]}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0,2], []], 2: [[1, 0], [1, 1], [], []]})
        strategy = Strategy(state, 2)
        assert strategy.zig_zag() == [0,3]

        state = GameState(board, {1: "black", 2: "white"}, [1, 2],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], []], 2: [[1, 0], [1, 1], [0, 3], []]})
        strategy = Strategy(state, 1)
        assert strategy.zig_zag() == [0,4]


        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [0, 4]], 2: [[1, 0], [1, 1], [0, 3], []]})
        strategy = Strategy(state, 2)
        assert strategy.zig_zag() == [1,2]

    def test_which_action_invalid_input(self):
        board = Board(2, 5, {}, num_of_fish_per_tile=2)

        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})

        strategy = Strategy(state, 2)
        with self.assertRaises(ValueError):
            strategy.which_action_to_take(0)

    def test_which_action_to_take_one_turn(self):
        board = Board(2, 5, {}, num_of_fish_per_tile=2)

        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})

        strategy = Strategy(state, 2)
        assert strategy.which_action_to_take(1) == ((1, 2), (0, 3))

    def test_which_action_to_take_multiple_turns(self):
        board = Board(4, 5, {}, num_of_fish_per_tile=2)

        state = GameState(board, {1: "black", 2: "white"}, [1, 2],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        board_tiles = board.get_tiles()
        board_tiles[0][1] = tile_inst(7)
        board_tiles[0][2] = tile_inst(12)
        strategy = Strategy(state, 1)
        assert strategy.which_action_to_take(2) == ((0, 2), (2, 2))

    def test_which_action_to_take_tiebreaker(self):
            # tests both cases of the tiebreaker
            board = Board(2, 5, {})

            state = GameState(board, {1: "black", 2: "white"}, [1, 2],
                              penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})

            strategy = Strategy(state, 1)
            assert strategy.which_action_to_take(1) == ((1, 3), (0, 3))



if __name__ == '__main__':
    unittest.main()