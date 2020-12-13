import sys
sys.path.append('../Common')
from game_tree import GameTree

"""
See state.py for details on what a GameState looks like

See game_tree.py for details on what a GameTree looks like

A strategy is a class, with attribute game_state, and another attribute player_id representing a player who is using
a given instance of this class. The purpose of this class is to provide methods for this player to strategize, by taking
care of two decisions: penguin placement and which action at a given state will result in the highest overall score (for a given number of turns). 
the game_state attr is the current game state of the game and the player_id attr is the id of the player whose turn it is currently in the game.
a player_id is a reference to a player; it will be determined by the tournament manager.

A Strategy does not need to have a GameTree passed in as an arg, as it can instantiate one from the GameState it is 
passed in, when it truly needs it in the which_action_to_take method. 
I did not want to unnecessarily instantiate and pass in a GameTree, if the player is only using this class for penguin placement 
strategizing, for example, since that method cannot use a GameTree.

An Action is a tuple of the form ((start_row, start_col), (dest_row, dest_col)). 
Where *row, and *col are both ints. (start_row, start_col) is the current location of a penguin, and (dest_row, dest_col) is
the location that the penguin wants to go to. See board.py for details on the coordinate system. An empty Action, representing
a time when a Player cannot make a move, is of the form ().

"""

# Class Signature: A Strategy is passed in two parameters, game_state (type is GameState) and player_id (type is int). A
# player_id is a reference to a Player; it will be determined by the tournament manager. For now, I thought it was
# necessary to deal with player ids as we don't have a Player class yet.

# Assumptions: This game state that is passed in is the CURRENT game state for which the game is not over, otherwise there would
# be no point of this class. I also assume that in the passed in game state, the turn is of the player who is
# represented by the passed in player_id (must match).


class Strategy:
    # Please see above for Class Signature & Assumptions
    def __init__(self, game_state, player_id):
        # This represents the current game state, is of type GameState
        self.__game_state = game_state
        # This represents the current game tree, is of type GameTree
        self.__game_tree = None
        # This represents the player id of the player using this Strategy instance, is of type int
        self.__player_id = player_id

    """
    Nothing -> Nothing
    
    Returns the next free spot available on the board, following a zig zag pattern that
    starts at the top left corner (when you reach the last column of a row, move to the row directly below). I interpret
    the top left corner as position [0,0] (row 0, column 0), the position directly to the right of it is [0,1]. The position
    directly below [0,0] is [1,0], etc. Please see board.py for more details on my coordinate system (which follows what I just described).
    
    There are no side effects because no game state is passed in; the referee will end up doing the placing based on
    what is returned by this function. 
    
    Assumption: The board has enough free slots for which penguins can be placed.
    """
    def zig_zag(self):
        board = self.__game_state.get_board()
        # Python ranges are exclusive at the end
        # i=0 i < len(board.get_tiles()) i++
        for i in range(0, len(board.get_tiles())):
            # j=0 j < (board.get_tiles())[i] j++
            for j in range(0, len(board.get_tiles()[i])):
                desired_posn = [i, j]
                if self.__game_state.is_unoccupied(desired_posn) and \
                        not self.__game_state.is_hole(desired_posn):
                            return desired_posn

    """
    int -> Action
    
    Picks the action that will realize the "best gain" (highest score/fish count) for the player whose turn it currently is,
    after looking ahead n > 0 turns in the tree. I return an Action because at the end of the day, the spec says that it 
    is a player's CHOICE OF ACTION, NOT THAT THE PLAYER HAS TO PERFORM THAT ACTION. If the game terminates before n turns
    can be executed, then it just takes the player's score at the node where the game ends. 
    
    If there is no Action to take, then it will return the empty Action that I described in the Action data def at the
    top of this file. Basically just an empty tuple ().
    
    """
    def which_action_to_take(self, n):
        if n == 0:
            raise ValueError("N must be greater than 0")

        # instantiates the game tree because now we need it (next_layer must still be called to kick off the generator)
        self.__game_tree = GameTree(self.__game_state)
        self.__game_tree.next_layer()

        actions_to_scores = {}
        for action, node in self.__game_tree.get_map_action_to_child_nodes().items():
            actions_to_scores[action] = (self.__minimax(node, n-1))

        # game over
        if actions_to_scores == {}:
            return ()

        # this is the best gain
        optimal_score = max(actions_to_scores.values())

        optimal_actions = [action for action in actions_to_scores if actions_to_scores[action] == optimal_score]

        return self.__get_optimal_action(optimal_actions)

    """
    GameTree int -> int

    Finds the best gain (highest score) that this Player can obtain after n turns, assuming that all other Players want to
    minimize this Player's gain, via the minimax algorithm. This will terminate because you can see that I have a base
    case where I stop if the appropriate number of turns has been played or if the game is over
    at the given state.
    """
    def __minimax(self, node, n):
        # base case, either the player has finished all their turns or there are no moves left after this move
        if n == 0 or node.get_game_state().is_game_over():
            return node.get_game_state().get_player_score(self.__player_id)
        # it is the maximizing player's turn
        if node.get_game_state().get_player_order()[0] == self.__player_id:
            value = float('-inf')  # because we need the absolute lowest possible value to compare to
            node.next_layer()
            for action, child_node in node.get_map_action_to_child_nodes().items():
                value = max(value, self.__minimax(child_node, n-1))
            return value
        # it is all opponents' turn
        else:
            value = float('+inf')  # because we need the absolute highest possible value to compare to
            node.next_layer()
            for action, child_node in node.get_map_action_to_child_nodes().items():
                value = min(value, self.__minimax(child_node, n))
            return value

    """
    [int] [Action] -> Action
    
    Finds the Action, out of all the possible candidate Actions leading to the best gain (highest fish count),
    that the player should take in order to obtain the best gain. If there are multiple Actions that can
    lead to the same gain, tiebreaker functionality is executed.
    """
    def __get_optimal_action(self, optimal_actions):
        # this means there are multiple optimal actions that can lead to the same best gain
        if len(optimal_actions) > 1:
            # tiebreaker for top most row of from position, top most col of from position
            optimal_actions = self.__tiebreaker(optimal_actions, 0)
            # tiebreaker top most row of to position, top most col of to position. It will terminate because there
            # cannot be two distinct Actions at the same time with the same from and to position: that would indicate duplicate Actions.
            if len(optimal_actions) > 1:
                optimal_actions = self.__tiebreaker(optimal_actions, 1)
            optimal_action = optimal_actions[0]
        else:
            optimal_action = optimal_actions[0]
        return optimal_action

    """
    [Action] int -> [Action]
    The which_pos arg is one of the indexes in an Action for either a start position or destination position.
    The start position is the first tuple in the Action, so index would be 0, and the destination position is the second tuple 
    in the Action, so index would be 1.
    
    Applies tiebreaker functionality to Actions.
    """
    @staticmethod
    def __tiebreaker(lo_actions, which_pos):
        # the list of different positions, either from or to positions
        lo_pos = []
        for action in lo_actions:
            lo_pos.append(action[which_pos])
        # finding the lowest row/ lowest column
        final_pos = (sorted(lo_pos))[0]
        final_actions = []
        for action in lo_actions:
            if action[which_pos] == final_pos:
                final_actions.append(action)
        return final_actions

    """
    Nothing -> GameState
    Getter method for the game state class attribute. 
    """
    def get_game_state(self):
        return self.__game_state

    """
    Nothing -> GameTree
    Getter method for the game tree class attribute. 
    """
    def get_game_tree(self):
        return self.__game_tree

    """
    Nothing -> int
    Getter method for the player id class attribute. 
    """
    def get_player_id(self):
        return self.__player_id
