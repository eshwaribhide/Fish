We are working in Python, an object-oriented language, so classes come into use.

**Data Representations for Game States:**

The game state itself will be represented by a class. This class has certain attributes.
 - Game pieces (game board, the tiles, and the penguin avatars). Each of these components has a **class** as its data representation. 
 - **List** of player objects
 - We anticipate that we will need to represent a player as a **class**, with functions that have the player strategy embedded in them. Therefore, we will refer to players as player objects.
 - **Dictionary** mapping a player object to the number of fish they currently have (int).
 - **Dictionary** mapping a player object to the row and column of the tile they are located on (**list** of row, col, which are both ints).
 - **Dictionary** mapping a player object to its avatar (a penguin object).
 - **Boolean** indicating whether the game is over or in progress.
 - Indication maybe **boolean** of a players turn and end, also for the rounds and dealers round (when you pay)
 - Event handler 
    - Tile clicked to indicate the change in games view, player points -- so valid tile move would indicate change
    - View change based on click or type of clicks (referee will tell the game state to update)
	

**External Interface Description**

Besides getter methods for all the attributes listed above (not enumerating them because it’s trivial), here are some other functions:

---
 Void function
 
 Initializes all aspects of the game, such as the game board, the players’ avatars, 
 each player’s fish count is set to 0.
 
 **def** initialize_game()

---
 Return bool (true if game is over, false if not)
 
 Checks whether the game is over, if there are no moves left to make (referee helps to
 determine this).
 
 **def** is_game_over()
 
---
 Return list of player objects
 
 Checks which players have the most fish. If there is a tie, will output all the player 
 objects that have the max number of fish. 
 
 **def** get_winner()

---
 Void function
 
 Renders the game board tiles with fish on them, and the avatars at their positions, and
 anything else that is front-end.
 
 **def** render_game()

---
 Player Object -> [player_current_row, player_current_col]
 
 Returns the position that a player is at, given a reference to it. Helpful for
 other players to make strategic decisions based on where to move.
 

 **def** get_player_position(player_object)
 
---
 Player Object -> Nothing (void function)
 
 Adds fish to a player object’s current fish count, if they moved to a tile 
 

 **def** add_fish(player_object)
 
---
 Player Object int int -> nothing (void function)
 
 Takes in a player object, a row, and a col, referee will determine based on the current 
 player’s position whether they can make the move
 
 
 **def** make_a_move(player_object, row, col)
 
---
 Player Object -> nothing (void function)
 
 Removes a player from the list of players if they have been terminated because of 
 malfunctioning software
 
 **def** remove_player(player_object)
 
 ---
 Void function
 
 Cleans up everything that needs to be cleaned up, such as destroying the tkinter
 instance.
 
 **def** cleanup_game()
