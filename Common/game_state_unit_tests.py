import unittest
from state import GameState
from board import Board


class TestGameState(unittest.TestCase):

    def test_is_pos_out_of_bounds(self):
        # tests out of bounds checker (row or col is either < 0 or >= # of rows or columns, since python indexing is
        #0-based)
        board = Board(4, 3, {})
        state = GameState(board, {1: "black", 2: "white"}, [1, 2])
        assert not state.is_pos_out_of_bounds([0,0])

        assert state.is_pos_out_of_bounds([-1,0])
        assert state.is_pos_out_of_bounds([0, -1])

        assert state.is_pos_out_of_bounds([10002, 0])
        assert state.is_pos_out_of_bounds([1, 10000])

    def test_player_has_penguin_at_pos(self):
        # tests whether a player has a penguin at a given posn
        board = Board(3, 2, {})
        state = GameState(board, {1: "black", 2: "white"}, [1, 2])
        assert not state.player_has_penguin_at_pos(1, [0, 0])
        assert not state.player_has_penguin_at_pos(1, [2, 1])

        state.place_avatar(1, [0, 0])
        assert state.player_has_penguin_at_pos(1, [0, 0])

        state.place_avatar(2, [0,1])
        assert state.player_has_penguin_at_pos(2, [0, 1])

        state.move_avatar(1, [0, 0], [2, 1])
        assert not state.player_has_penguin_at_pos(1, [0, 0])
        assert state.player_has_penguin_at_pos(1, [2, 1])

    def test_is_unoccupied(self):
        # tests that a tile is unoccupied
        board = Board(3, 2, {})
        state = GameState(board, {1: "brown", 2: "red"}, [1, 2])
        assert state.is_unoccupied([0,0])

        state.place_avatar(1, [0, 0])
        assert not state.is_unoccupied([0, 0])

    def test_is_hole(self):
        # tests whether a given posn is a hole.
        board = Board(4, 3, {1: [0]})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])
        assert state.is_hole([1,0])

        state.place_avatar(2, [0,0])
        assert not state.is_hole([0,0])

        state.place_avatar(1, [0, 1])
        assert not state.is_hole([0, 1])

        state.move_avatar(2, [0,0], [2,0])
        assert state.is_hole([0,0])

    def test_is_placement_phase_over(self):
        # tests whether the placement phase can be judged as in progress or over
        board = Board(4, 3, {1: [0]})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])

        assert not state.is_placement_phase_over()

        board = Board(4, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})

        assert state.is_placement_phase_over()

    def test_turn_taking(self):
        # tests the enforcement of turn taking
        board = Board(4, 3, {1: [0]})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])

        # not your turn, so cannot move
        assert not state.place_avatar(1, [0,0])

        # your turn, so you can go
        assert state.place_avatar(2, [0, 0])

        # now your turn, so you can go
        state.place_avatar(1, [0, 1])

    def test_place_avatar(self):
        # tests placement functionality. makes sure it doesn't work for bad cases. the function will return
        # false if it didn't go through with the placement.
        board = Board(4, 3, {})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])
        # out of bounds case
        assert not state.place_avatar(1, [-1,0])
        assert not state.player_has_penguin_at_pos(1, [-1, 0])

        # avatar is already there
        assert state.place_avatar(2, [0,0])
        state.place_avatar(2, [0,0])
        assert state.player_has_penguin_at_pos(2, [0,0])
        assert not state.place_avatar(1, [0,0])
        assert not state.player_has_penguin_at_pos(1, [0, 0])

        # hole
        board = Board(4, 3, {1:[0]})
        state = GameState(board, {1: "black", 2: "white"}, [1, 2])
        assert not state.place_avatar(1, [1, 0])
        assert not state.player_has_penguin_at_pos(1, [1, 0])

        # general case
        board = Board(4, 3, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [1, 2])
        assert state.place_avatar(1, [1, 0])
        assert state.player_has_penguin_at_pos(1, [1, 0])

    def test_move_avatar(self):
        # tests moving functionality. makes sure it doesn't work for bad cases. the function will return
        # false if it didn't go through with the moving.
        board = Board(4, 3, {}, num_of_fish_per_tile=3)
        state = GameState(board, {1: "black", 2: "white"}, [1, 2])
        # out of bounds case
        # player 1 first placement
        assert state.place_avatar(1, [1, 0])
        assert not state.move_avatar(1, [1,0], [-1, 0])
        assert not state.player_has_penguin_at_pos(1, [-1, 0])

        # avatar is already there
        assert state.place_avatar(2, [2, 1])
        # player 2 first placement
        state.place_avatar(2, [2, 1])
        assert state.player_has_penguin_at_pos(2, [2, 1])
        assert not state.move_avatar(1, [1, 0], [2, 1])
        assert not state.player_has_penguin_at_pos(1, [2, 1])

        # player doesn't have a penguin at the start posn
        assert not state.move_avatar(1, [3,2], [1,2])

        # posn is not reachable
        assert not state.move_avatar(1, [1,0], [3,2])

        # desired posn is a hole
        # player 1 second placement/move
        assert state.move_avatar(1, [1,0], [3,0])
        assert not state.move_avatar(2, [2,1], [1,0])

        # general case, player 2 second placement/move
        assert state.move_avatar(2, [2, 1], [3, 1])

        player_fish_count = state.get_player_fish_count()
        assert player_fish_count[1] == 3
        assert player_fish_count[2] == 3

    def test_remove_player(self):
        # tests player removal
        board = Board(2, 5, {})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])
        assert state.get_player_penguin_colors() == {1: "black", 2: "white"}
        assert state.get_player_order() == [2, 1]
        assert state.get_player_fish_count() == {1: 0, 2: 0}
        assert state.get_penguin_posns() == {1: [[], [], [], []], 2: [[], [], [], []]}

        state.remove_player(1)
        assert state.get_player_penguin_colors() == {2: "white"}
        assert state.get_player_order() == [2]
        assert state.get_player_fish_count() == {2: 0}
        assert state.get_penguin_posns() == {2: [[], [], [], []]}

    def test_get_all_rechable_dests(self):
        # tests getting all the reachable destination positions
        board = Board(2, 5, {})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])
        assert state.place_avatar(2, [1, 0])
        assert state.place_avatar(1, [0, 0])

        assert state.place_avatar(2, [1, 1])
        assert state.place_avatar(1, [0, 1])

        assert state.place_avatar(2, [1, 2])
        assert state.place_avatar(1, [0, 2])

        assert state.place_avatar(2, [1, 3])
        assert state.place_avatar(1, [0, 3])

        assert state.get_all_reachable_dests(2) == [[0, 4]]

    def test_get_player_score(self):
        # tests getting the score for a particular player
        board = Board(2, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])
        assert state.place_avatar(2, [1, 0])
        assert state.place_avatar(1, [0, 0])

        assert state.get_player_score(2) == 0
        assert state.get_player_score(1) == 0

        assert state.move_avatar(2, [1, 0], [0,1])
        assert state.get_player_score(2) == 2

    def test_is_game_over_and_turn_skipping(self):
        # tests that the game is over when there are no reachable posns
        board = Board(2, 5, {})
        state = GameState(board, {1: "black", 2: "white"}, [2, 1])
        assert state.place_avatar(2, [1, 0])
        assert state.place_avatar(1, [0, 0])

        assert state.place_avatar(2, [1, 1])
        assert state.place_avatar(1, [0, 1])

        assert state.place_avatar(2, [1, 2])
        assert state.place_avatar(1, [0, 2])

        assert state.place_avatar(2, [1, 3])
        assert state.place_avatar(1, [0,3])

        assert not state.is_game_over()

        # create a hole
        assert state.move_avatar(2, [1, 3], [0,4])

        # nowhere player 1 can go
        assert state.skip_turn(1)

        # # create another hole
        assert state.move_avatar(2, [0, 4], [1, 4])

        # nowhere left for anyone to go
        assert state.is_game_over()


if __name__ == '__main__':
    unittest.main()
