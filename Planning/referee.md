I am working in Python, an object-oriented language, so classes come into use.

**Purpose: The purpose of this structure is to serve as a game supervisor.**

**Who is Using This Structure? The tournament manager will directly instantiate it.**

**Data Representations for Referees:**
I assume that since the tournament manager sets up the players, it will determine the Player order. 
A referee can be CREATED BY THE TOURNAMENT MANAGER SIMPLY BY INSTANTIATING A REFEREE CLASS.

Currently, in all my classes, I have this notion of a player id, which is an int that refers to a player. I assume that the tournament manager
will deal with this assignment.

First of all, a Referee class constructor should take in the list of player ids IN PLAYER ORDER (youngest player's player id first) and the board dimensions (int val of rows, int val of columns), 
according to the Fish spec. A referee itself should also have its own class attributes: the current game state (a GameState object) and the
current game tree for that state (a GameTree object). The current game state has the board "embedded" into it. These
attributes are necessary for a referee to keep a hold on the game. 

The referee class will ALSO keep track of failing/cheating players via a class attribute, a list of player ids called bad_players.


**Referee API**

---
 Nothing -> Nothing
 
 In this method, the referee will SET UP A BOARD object, by instantiating it by passing in the dimensions it got from the tournament manager, and the locations
 of the holes THAT THE REFEREE CHOOSES. It may also specify the minimum number of one fish tiles and/or the number of fish per tile
 IF THE REFEREE FEELS LIKE IT.
 The referee will then determine penguin colors. 
 
 Then the referee should instantiate a GameState object and set its current game state attribute to that GameState. With this GameState,
  the referee should instantiate a GameTree object and set its current game tree attribute to that GameTree, in order to complete the setup.
 
 **def** __setup()

 

---

Nothing -> Outcome (where Outcome is a Dictionary of the form {"won": List of Player objects, "lost": List of Player objects, 
"cheated/failed": List of Player objects}.)

This is kind of the "main" method for the referee. Here, the referee will interact with the players, asking
them to place a penguin (if game state placement phase is not over) or make a move, for example, and checking their moves, and the referee will keep the game running with this method, like
with a while loop.
This method will terminate/the while loop will break whenever the game is over (when no moves are left for any player), which the referee can check through the current game state's
is_game_over() method.

**def** run_game()

---

Nothing -> Nothing

This is a void method. This function will just call
the GameState's remove_player method, which erases all knowledge of a player's **penguins** from the game.

Also, the Player will be added to the referee's bad_players attr, which is a list of failing/cheating player ids.

**def** __remove_player(Player)

___
MAY ADD LATER, BUT NOT NECESSARY NOW
Nothing -> Nothing

This shuts down a game, does all the cleanup, and outputs a dictionary mapping each player to their respective status. It will be called
when the game is over (there are no moves left for any player). At the end of this method, the referee will call
each player's game_is_over() method to signal to them that the game is over, and will also report to them the game
outcome, probably via a Status, where Status is "won", "lost", or "cheated".According to the spec, if several players caught the same number of fish, they are all winners.
If
a player didn't have the highest number of fish, they are losers. If a player is in the Referee's bad_players class attr, then
their Status is "cheated".

**def** end_game()

---
Nothing -> Outcome, where Outcome is a Dictionary of the form {"won": List of Player objects, "lost": List of Player objects, 
"cheated/failed": List of Player objects}.
where Status is "won", "lost", or "cheated". According to the spec, if several players caught the same number of fish, they are all winners. If
a player didn't have the highest number of fish, they are losers. If a player is in the Referee's bad_players class attr, then
their Status is "cheated".

This reports/broadcasts the outcome of the game: who won, who lost, and who failed/cheated. 

**def** __report_outcome()


---
MAY ADD LATER WHEN OBSERVERS GET INVOLVED.
Nothing -> Action
Or
Nothing -> [Action]
Reports ongoing actions to game observers, probably the action that the current player decided to take or the list of the
Actions that the current player COULD take.

**def** report ongoing_actions()