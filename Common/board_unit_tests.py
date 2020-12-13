import unittest
from board import Board
from tile_fish_penguin_constants import MAX_FISH


class TestBoard(unittest.TestCase):

    def test_non_int_row_or_col(self):
        with self.assertRaises(TypeError):
            # tests that row and col should be ints
            Board('hello', 2, {})
            Board(2, [], {})

    def test_too_few_rows_or_col(self):
        with self.assertRaises(ValueError):
            # tests that rows and cols should be >= 1
            Board(-1, 2, {})
            Board(2, 0, {})

    def test_wrong_holes_type(self):
        # tests that holes is of the form int key: [[int]] val
        with self.assertRaises(TypeError):
            # not a dict
            Board(1, 1, [])
            # not a dict with int keys
            Board(1, 1, {"hello": []})
            # not a dict with int key: [] val
            Board(1, 1, {0: "hello"})
            # not a dict with int key: [[int]] val
            Board(1,1, {0: ["hello"]})

    def test_wrong_min_num_one_fish_tiles_type(self):
        with self.assertRaises(TypeError):
            # tests that min num one fish tiles needs to be an int type
            Board(1, 1, {}, min_num_one_fish_tiles='hello')
            Board(1, 1, {}, min_num_one_fish_tiles=[])

    def test_wrong_min_num_one_fish_tiles_val(self):
        # tests that min num one fish tiles needs to be >=0 and < row*column (total tiles)
        with self.assertRaises(ValueError):
            # less than 0
            Board(1, 1, {}, min_num_one_fish_tiles=-1)
            # greater than the number of tiles on the board (row*columns)
            Board(4, 3, {}, min_num_one_fish_tiles=20)

    def test_wrong_num_of_fish_per_tile_type(self):
        # tests that num fish per tile is an int
        with self.assertRaises(TypeError):
            # needs to be an int type
            Board(1, 1, {}, num_of_fish_per_tile='hello')
            Board(1, 1, {}, min_num_fish_per_tile=[])

    def test_wrong_num_of_fish_per_tile_val(self):
        # tests that num fish per tile is in the bounds of >=1 and <= max fish
        with self.assertRaises(ValueError):
            # less than 1
            Board(1, 1, {}, num_of_fish_per_tile=-1)
            # greater than max fish
            Board(4, 3, {}, num_of_fish_per_tile=MAX_FISH + 1)

    def test_conflict_min_num_one_fish_tiles_num_of_fish_per_tile(self):
        # tests for conflicting parameters given
        with self.assertRaises(ValueError):
            # asking for 3 fish per tile, but then asking for 2 one fish tiles, impossible
            Board(4, 3, {}, num_of_fish_per_tile=3, min_num_one_fish_tiles=2)

    def test_intialize_game_board_dimensions(self):
        # tests just checking that there are 3 sublists and that each sublist has 2 elements, in order to
        # validate that the board dimensions are correct
        board = Board(3, 2, {})
        exp_row_count = 3
        exp_col_count = 2
        actual_row_count = 0
        board_tiles = board.get_tiles()
        for i in board_tiles:
            actual_row_count += 1
            actual_col_count = 0
            for _j in i:
                actual_col_count += 1
            assert actual_col_count == exp_col_count
        assert actual_row_count == exp_row_count

    def test_initialize_game_board_holes(self):
        # tests that the holes are where they should be
        exp_holes = {0: [0, 1], 1: [0]}
        actual_holes = {}

        board = Board(3, 2, exp_holes)
        board_tiles = board.get_tiles()

        for i in range(len(board_tiles)):
            for j in range(len(board_tiles[i])):
                tile = board_tiles[i][j]
                tile_vis = tile.get_visibility()
                if not tile_vis:
                    if i in actual_holes:
                        actual_holes[i].append(j)
                    else:
                        actual_holes[i] = [j]
        assert exp_holes == actual_holes

    def test_initialize_game_board_min_num_one_fish(self):
        # tests that min num of one fish tiles is as expected
        board = Board(3, 2, {}, min_num_one_fish_tiles=2)
        exp_min_num_one_fish_tile = 2
        board_tiles = board.get_tiles()

        actual_num_one_fish_tile = 0
        for i in range(len(board_tiles)):
            for j in range(len(board_tiles[i])):
                tile = board_tiles[i][j]
                tile_fish_count = tile.get_num_fish_per_tile()
                if tile_fish_count == 1:
                    actual_num_one_fish_tile += 1
        assert exp_min_num_one_fish_tile <= actual_num_one_fish_tile

    def test_initialize_game_board_num_of_fish_per_tile(self):
        # tests that num of fish per tile is as expected
        board = Board(3, 2, {}, num_of_fish_per_tile=2)
        exp_tile_fish_count = 2
        board_tiles = board.get_tiles()

        for i in range(len(board_tiles)):
            for j in range(len(board_tiles[i])):
                tile = board_tiles[i][j]
                tile_fish_count = tile.get_num_fish_per_tile()
                assert tile_fish_count == exp_tile_fish_count

    def test_get_reachable_posns_empty_tile(self):
        # tests that you can't get reachable posns from an empty tile
        with self.assertRaises(ValueError):
            board = Board(4, 3, {0:[0]})
            board.get_reachable_posns([0, 0], [])

    def test_get_reachable_posns_out_of_bounds(self):
        # tests that you can't get reachable posns from a non-existent tile (out of bounds)
        with self.assertRaises(ValueError):
            board = Board(4, 3, {})
            board.get_reachable_posns([7, 3], [])

    def test_get_reachable_posns(self):
        # tests all different directions
        board = Board(8, 3, {})
        exp_reachable_posns = [[1, 0], [2, 1], [1, 1], [0, 2], [4, 1], [5, 1], [6, 2], [7, 2], [5, 0], [7, 0],
                                   [4, 0], [2, 0]]
        actual_reachable_posns = board.get_reachable_posns([3, 0], [])
        assert exp_reachable_posns == actual_reachable_posns

        # tests holes effect
        board = Board(3, 3, {})
        exp_reachable_posns = [[0, 2], [1, 2], [1, 1], [0, 1]]
        actual_reachable_posns = board.get_reachable_posns([2, 2], [])
        assert exp_reachable_posns == actual_reachable_posns

        board = Board(3, 3, {0:[2]})
        exp_reachable_posns = [[1, 2], [1, 1], [0, 1]]
        actual_reachable_posns = board.get_reachable_posns([2, 2], [])
        assert exp_reachable_posns == actual_reachable_posns

    def test_remove_tile_out_of_bounds(self):
        # tests that a non-existent tile cannot be removed (out of bounds)
        with self.assertRaises(ValueError):
            board = Board(4, 3, {})
            board.remove_tile([7, 3])

    def test_remove_tile_already_removed(self):
        # tests that an already removed tile cannot be removed
        with self.assertRaises(ValueError):
            board = Board(4, 3, {0:[0]})
            board.remove_tile([0, 0])

    def test_remove_tile(self):
        # tests the effect of removing a tile, its visibility should be set to False
        board = Board(4, 3, {})
        board_tiles = board.get_tiles()
        tile = board_tiles[0][0]
        assert tile.get_visibility()

        board.remove_tile([0,0])
        assert not tile.get_visibility()


if __name__ == '__main__':
    unittest.main()