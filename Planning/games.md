I am working in Python, an object-oriented language, so classes come into use.

**Purpose: The purpose of this structure is to provide a tree of all potential moves in any state reachable 
from a given starting point (generally the state in which all penguins have been placed). This helps referees and players
with rule checking, and players with planning ahead.**

**Who is Using This Structure? Referees and players.**

**Data Representations for Games:**
It seems like a Game can be represented by a class and can have an attribute called
game_tree. This fulfills the requirements of a game being a tree of all potential moves in any state reachable 
from a given starting point. In terms of designing the Tree

- The Tree will be a **dictionary**, as they provide nice abilities for nesting, which
is important in this Tree structure, and they provide easy lookup access. 
I want the Tree to look like this: 
{GameState:{GameState: {GameState...}, GameState: {GameState...}}} etc

In terms of data types, GameState is an instance of the GameState class. 

Now for an explanation...in the form of FAQs
  - What does the Games class constructor look like?
    - The root of the tree, a key, is the starting point: a state in which all players have placed all 
     their available penguins. So the Games class constructor will take in a GameState instance to be that start state.
  - How is game_tree a tree of moves? Looks like a tree of game states?
    - It does not make sense, and is rather brittle, to have the root of the tree to be a state and the rest
    of the layers be a list of moves. Because, each list of moves is going to be dependent on the game state
    at that point in time. For example, a position may be reachable in one state and not
    in another (maybe a hole was created in the middle because someone moved, etc). 
  - But still, how is this a tree of moves?
    - Because, the GameState class has an attribute called penguin_positions. And this data
    structure maps a player id to all its different player positions. Therefore, for a child GameState, this represents 
    a move in a way, as it represents the destination positions for a Penguin, where the origin
    positions will be those positions that belong to the parent GameState (in the layer above)
 - How does the tree child node determination work?
    - The tree of moves will be very large. Essentially, a parent node will have child nodes that are
  all the permutations of moves, possible, and for all a player's penguins, based on whose turn it currently is.  So, let's say our parent node is the start state. Then, one child
  node is the state resulting from when player 1 moves its penguin1 to [x,y]. Another child node could be the state resulting from when player 1 moves its penguin1 to [x,z]. Another
  possibility is the state resulting from when player 1 moves its penguin**2** to [x,y] (not penguin1).
  Really, there are a lot of combinations. Now, each of those moves results in new penguin positions. These
  will be passed in to the constructor of a GameState object, which is the official child node (type).
 
  

  
**External Interface Description**
The only attribute in the Game class will be game_tree. So it is necessary to have a getter method for it,
so that referees and players can look at it as a whole. However, there are some methods that
can help referees and players to get more understandable data.

1. Before these next ones, **yes, I do have the option for an intermediate Games tree**. Because, my GameState
supports intermediate GameState construction. And so, you can really create a Games tree by passing in any
sort of GameState. Therefore, if the GameState you pass in isn't technically the start state, it will still
be treated as the start state for the Games tree. And be the root of the tree. So you can get all moves from then on.



---
 int [int,int] [int,int] ->bool
 
 Checks if a move from start to destination is valid, and returns true if that is the case. Start and destinations are
 positions in the form [row, col]. Useful for both players and referees.
 
 **def** is_move_valid(player_id, start, destination)
 
---
Nothing (uses class variable) -> Dict
 
 A getter method for the whole entire game tree. Useful
 for players to see what another player may do as their next move, or to see what they have
 as options for their next moves. Also useful for the referee for validity checks.
 
 **def** get_game_tree()

---
int -> Dict
 
 Uses the player id, finds their entire tree of moves from the game_tree attribute. Useful
 for players to see what another player may do as their next move, or to see what they have
 as options for their next moves.
 
 **def** get_players_move_choices_total(player_id)
 
---
 GameState -> Dict
 
Return the game tree from "here on out", meaning, given a game state, it will return all the
moves that are **left** after. It's helpful because the game tree is a large structure, so maybe
you can eliminate unnecessary info for games that have already passed.

 **def** get_players_move_choices_from_here(game_state)
 
---
Int GameState -> List(Dict)
The return type is a List(Dict), meaning
[{"start":[row,col], "end":[row,col]},
 {"start":[row,col], "end":[row,col]}] where start/end are strings and row col are
both ints
 
Returns the next 2 moves that would maximize the player's fish count, ideally via
positions that other penguins cannot move to. I don't think it makes sense to do
anything past 2 because the game state could change tremendously. This
can help a player always be 2 steps ahead, which is good enough.

 **def** which_next_2_moves_give_me_the_most_fish(player_id, game_state)
