import copy

"""
A GameTree is a class that represents an entire game, all possible permutations of where players might place their
penguins. Each tree node is either a leaf (aka a game over node) or an internal node (has child GameTrees). My structure fits the definition
of (GameState, Dict(Action -> GameTree)). This means that the "data" of the GameTree is of type GameState, and each tree
has a class variable of the type Dict(Action -> GameTree) that maps each "edge" (representing a legal Action) 
to each legal successor GameTree that will result from taking that Action. I call this class variable map_action_to_child_nodes. It is assumed
that the GameState given to a GameTree has completed the penguin placement phase.

"game over" Nodes, aka leaves, will have an empty map_action_to_child_nodes, since there are no legal actions or legal child trees. So
it will look like {}.

"can make a move" Nodes will have general Dict(Action -> GameTree), as many actions as there possible are and all the child
trees that result from those actions.

"player stuck" nodes will have their map_action_to_child_nodes looking like {():GameTree}. There are no legal actions to take,
since the player is stuck, and the only GameTree to map to is essentially the same exact GameTree, just with player order
cycled to the next player in the GameState.

An Action is a tuple of the form ((start_row, start_col), (dest_row, dest_col)). 
Where *row, and *col are both ints. (start_row, start_col) is the current location of a penguin, and (dest_row, dest_col) is
the location that the penguin wants to go to. See board.py for more information on my coordinate system. An empty Action, 
representing a time when a Player cannot make a move, is of the form ().

"""


class GameTree:
    def __init__(self, game_state):
        assert game_state.is_placement_phase_over(), "State is invalid, penguin placement phase " \
                                                     "is still ongoing"

        self.__game_state = game_state

        # this is a Dict of the type (Action -> GameTree) that maps each "edge" (legal action) to each legal successor
        # GameTree that will result from taking that Action.
        self.__map_action_to_child_nodes = {}

        # This is basically this is the tree cache...these are the "last" tree nodes that were generated in the
        # __generate_game_tree function that will need to have their child nodes computed in the next iteration of
        # the generator. That way you do not have to keep exploring the tree recursively till you find the layer that does not
        # have its child nodes set yet.
        self.__last_nodes = []

    """
    Nothing -> Nothing
    
    A generator function generating a layer of the game tree at every iteration. This does NOT generate the whole tree
    at once, so the generation is "suspended/frozen" until the next_layer() method is called by the user, which will 
    advance the generator. Essentially, this method generate_game_tree is never called directly; that is why it is private.
    """
    def __generate_game_tree(self):
        while True:
            if self.__map_action_to_child_nodes == {}:
                self.__map_action_to_child_nodes = self.all_actions_to_child_nodes()
                for action, child_node in self.__map_action_to_child_nodes.items():
                    self.__last_nodes.append(child_node)
                yield
            else:
                new_last_nodes = []
                for child_node in self.__last_nodes:
                    child_node.__map_action_to_child_nodes = child_node.all_actions_to_child_nodes()
                    for action2, child_node2 in child_node.__map_action_to_child_nodes.items():
                        new_last_nodes.append(child_node2)
                # represents the fact that the game is over because for each node in the current layer there were
                # no child nodes for any of them
                if new_last_nodes == []:
                    break
                self.__last_nodes = new_last_nodes
                yield

    """
    Nothing (uses class variables) -> Nothing (if we are not done with the game for all parent states)
    Nothing -> String (if we are indeed done with the game for all parent states)
    
    A wrapper method for the build in "next" method, used to advance a generator. 
    
    Return "GameDone" if the game is over for all parent nodes in the last computed layer of the tree.
    
    """
    def next_layer(self):
        try:
            next(self.__generate_game_tree())
        except StopIteration:
            return "Game Done"

    """
    int, {int: [int, int]}, GameState, [GameState]  -> Nothing
    Helps to find all the legal successor states (child states) for a given game state.
    """
    def __get_all_actions_to_child_nodes_help(self, whose_turn, player_penguin_posns, game_state):
        all_actions_to_child_nodes = {}
        for i in range(len(player_penguin_posns)):
            start_posn = player_penguin_posns[i]
            all_dests = game_state.get_all_reachable_dests(whose_turn, which_penguin=i)
            for dest_posn in all_dests:
                game_state_copy = copy.deepcopy(game_state)
                game_state_copy.move_avatar(whose_turn, start_posn, dest_posn)
                all_actions_to_child_nodes[(tuple(start_posn), tuple(dest_posn))] = GameTree(game_state_copy)
        return all_actions_to_child_nodes

    """
    GameState -> [GameState]
    Gets all the legal successor states (child states) for a given game state.
    
    Return a List of GameStates that are legal successor states of the given game state. If the game is over at the
    given game state, then I return an empty list [].
    """
    def all_actions_to_child_nodes(self):
        # "game over" node
        if self.__game_state.is_game_over():
            return {}

        game_state_player_order = self.__game_state.get_player_order()
        game_state_penguin_posns = self.__game_state.get_penguin_posns()

        whose_turn = game_state_player_order[0]

        game_state_copy = copy.deepcopy(self.__game_state)

        # "player stuck" node
        if game_state_copy.skip_turn(whose_turn):
            return {(): GameTree(game_state_copy)}

        # general "can make a move" node
        else:
            player_penguin_posns = game_state_penguin_posns[whose_turn]
            return self.__get_all_actions_to_child_nodes_help(whose_turn, player_penguin_posns, self.__game_state)

    """
    Action -> bool (Illegal move)
    Action -> GameState (Legal move)
    
    If the action is illegal, then I signal this by returning False. Otherwise, I return the GameState that would result 
    from performing the action by seeing whether this Action is present in the root node's map_action_to_child_nodes and 
    its linked child GameTree's GameState.
    
    """
    def execute_action(self, action):
        for legal_action in self.__map_action_to_child_nodes:
            if action == legal_action:
                child_node = self.__map_action_to_child_nodes[legal_action]
                return child_node.get_game_state()
        return False

    """
    func -> Nothing (void function, if func is a render_game_state function)
    func -> [Real] 
    
    Emulates the 'map' function in a way. Given a function, it applies this function to all of the game states that are 
    legal successor states of the root node's game state.
    """
    def apply_to_all_children(self, func):
        res = []

        for child_node in self.__map_action_to_child_nodes.values():
            child_node_state = child_node.get_game_state()
            res.append(func(child_node_state))

        # None will be in res if func was void and had no return. If func is void, then
        # I want to keep this function matching that signature. So it will be void, too, by
        # not returning anything.
        if None not in res:
            return res

    """
    GameState -> int
    A sample method that can be used in the apply_to_all_children method as a function object. It
    maps each game state to the fish count of the player who just played during the state right before
    the given state (the previous player).
    
    Returns the score of the previous player.
    """
    @staticmethod
    def score_at_state(game_state):

        game_state_player_order = game_state.get_player_order()
        previous_player = game_state_player_order[-1]
        return game_state.get_player_score(previous_player)

    """
    GameState -> Nothing (Void function)
    A sample method that can be used in the apply_to_all_children method as a function object, and it's
    a wrapper method for the render game state method.
    """
    @staticmethod
    def render(game_state):
        game_state.render_game_state()

    """
    Nothing -> GameState
    Getter method for the game_state class variable.
    """
    def get_game_state(self):
        return self.__game_state

    """
    Nothing -> {Action: GameTree}
    Getter method for map_action_to_child_nodes class variable.
    """
    def get_map_action_to_child_nodes(self):
        return self.__map_action_to_child_nodes

    """
    Nothing -> [GameTree]
    Getter method for last_nodes class variable.
    """

    def get_last_nodes(self):
        return self.__last_nodes
