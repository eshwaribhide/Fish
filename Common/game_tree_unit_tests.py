import unittest
from state import GameState
from board import Board
from game_tree import GameTree


def get_parents_children_count(game_tree_slice):
    """
    Util method for tests to check number of parent and child nodes.
    """
    parent_count = 0
    child_count = 0
    for k, val in game_tree_slice.items():
        parent_count += 1
        for child_node in val:
            child_count += 1
    return {"parents": parent_count, "children": child_count}


class TestGameTree(unittest.TestCase):

    def test_penguin_placement_ongoing(self):
        # tests that a GameTree cannot be made if the placement phase is still going on for its initial state
        with self.assertRaises(AssertionError):
            board = Board(2, 5, {}, num_of_fish_per_tile=2)
            state = GameState(board, {1: "black", 2: "white"}, [2, 1])
            GameTree(state)

    def test_game_tree_one_layer(self):
        # tests that the child nodes have the right turn and have added holes in the board, indicating a move being made
        board = Board(4, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        game = GameTree(state)

        game.next_layer()

        assert len(game.get_map_action_to_child_nodes()) == 19

        for action, child_node in game.get_map_action_to_child_nodes().items():
            assert child_node.get_map_action_to_child_nodes() == {}

        game.next_layer()

        game_tree_child_1 = game.get_map_action_to_child_nodes()[((1, 0), (2, 1))]

        assert game_tree_child_1.get_game_state().get_player_order() == [1, 2]
        assert len(game_tree_child_1.get_game_state().get_board().get_holes()) == 1

        game_tree_child_2 = game.get_map_action_to_child_nodes()[((1, 0), (3, 1))]
        assert game_tree_child_2.get_game_state().get_player_order() == [1, 2]
        assert len(game_tree_child_2.get_game_state().get_board().get_holes()) == 1




    def test_game_tree_complete_depth(self):
        # tests that the depth of the complete game tree is as expected
        board = Board(2, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        game = GameTree(state)
        game.next_layer()
        game.next_layer()
        assert game.next_layer() == "Game Done"




    def test_execute_action_legal(self):
        # tests the behavior of execute_action with regards to a legal move
        board = Board(4, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        game = GameTree(state)


        game.next_layer()

        assert game.execute_action(((1, 0), (3, 0)))

        game.next_layer()

        game_tree_child_1 = game.get_map_action_to_child_nodes()[((1, 0), (3, 0))]

        assert game_tree_child_1.execute_action(((0,0), (2,0)))


    def test_execute_action_illegal(self):
        # tests the behavior of execute_action with regards to an illegal move
        board = Board(4, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        game = GameTree(state)

        game.next_layer()
        assert not game.execute_action(((-1,0), (3,0)))
        assert not game.execute_action(((1, 0), (4, 0)))


    def test_apply_to_all_children(self):
        # tests the apply to all children method
        board = Board(2, 5, {}, num_of_fish_per_tile=2)
        state = GameState(board, {1: "black", 2: "white"}, [2, 1],
                          penguin_posns={1: [[0, 0], [0, 1], [0, 2], [1, 3]], 2: [[1, 0], [1, 1], [1, 2], [1, 4]]})
        game = GameTree(state)

        game.next_layer()

        assert game.apply_to_all_children(game.score_at_state) == [2, 2]

        game.next_layer()

        game_tree_child_1 = game.get_map_action_to_child_nodes()[((1, 2), (0, 3))]
        assert game_tree_child_1.apply_to_all_children(game.score_at_state) == [2]

        game_tree_child_1 = game.get_map_action_to_child_nodes()[((1, 4), (0, 4))]
        assert game_tree_child_1.apply_to_all_children(game.score_at_state) == [2]



if __name__ == '__main__':
    unittest.main()