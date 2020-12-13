import unittest
import sys
from referee import Referee
sys.path.append('../Common')
from board import Board
sys.path.append('../Player')
from player import Player


class TestReferee(unittest.TestCase):

    def test_run_game_1(self):
        board = Board(2, 5, {}, num_of_fish_per_tile=2)
        player1 = Player(1)
        player2 = Player(2)
        player_seq = [player1, player2]
        referee = Referee(player_seq, test_board=board)
        assert referee.run_game() == {'won': [player1], 'lost': [player2], 'cheated/failed': []}

    def test_run_game_2(self):
        board = Board(4, 3, {3:[0]}, num_of_fish_per_tile=2)
        player1 = Player(1)
        player2 = Player(2)
        player_seq = [player2, player1]
        referee = Referee(player_seq, test_board=board)
        assert referee.run_game() == {'won': [player2], 'lost': [player1], 'cheated/failed': []}

    def test_run_game_tie(self):
        board = Board(2, 5, {0: [0, 1]}, num_of_fish_per_tile=2)
        player1 = Player(1)
        player2 = Player(2)
        player_seq = [player1, player2]
        referee = Referee(player_seq, test_board=board)
        assert referee.run_game() == {'won': [player1, player2], 'lost': [], 'cheated/failed': []}


if __name__ == '__main__':
    unittest.main()