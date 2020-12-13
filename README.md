**Fish** :fish:

Overall Assignment Purpose: Fish is a board game for two to four players. 
The game board is a grid of hexagonal tiles, each of which displays a positive number of fish.
The player avatars come in the shape of penguins, which of course eat fish.
The goal of the game is to collect as many fish as possible. We need to design and implement Fish, construct the tournament management system, and connect the manager to "house players" along with remote players.

**Fish: Games!**

From Fish: Strategy - The strategy representation hat takes care of penguin placements and a choice of action for the player whose turn it is has been completed
From Fish: GameTree - The game tree representation has been completed, along with query functionality to determine legality of a move and the effects of a function on a parent node's children.

From Fish: GameState - The game state data and visual representations have been completed. 

From Fish: GameBoard – The board and tile data representations have been completed, along with visual representations of Fish and Penguins.

The purpose of this assignment is to
 - Create implementations for the Player and Referee

**Where To Find What** 😬

***Repo Level Directory Fish (Root Folder):***

 - Contains the README.md. (aka this file)
 - Contains the directories **Admin**, Player, Common, Planning.
 - Contains the unit test script 'xtest'. (a script to run all the unit tests. Scroll down to see how to run it).
 
***Repo Level Directory 3, 4, 5, 6:***
 - Each contain the subdirectories Other and Tests, along with exe test harnesses
 - 3: xboard, 4: xstate, 5: xtree, **6: xstrategy**
 - Details come after the details for Common & Planning (scroll down)
 
**Sub-Directory Admin:**
- **This folder contains all the components related to the Referee and the Tournament Manager.**

- **Contains referee implementation (referee.py)**
- **Contains manager interface (manager_interface.py)**
- **Contains referee unit tests (referee_unit_tests.py)**

Sub-Directory Player:

- This folder contains all the components related to a Player, such as an implementation and to strategize.

- **Contains player implementation (player.py).**

- Contains strategy source code (strategy.py). Has all the functionality related to
a potential penguin placement strategy/choosing which action is best to take at a point in time

- Contains strategy unit tests (strategy_unit_tests.py)

- **Contains player unit tests (player_unit_tests.py)**

Sub-Directory Common:

- This folder contains all of the components of the game, such as data representations
of the game state, board, and tiles, along with fish and penguin images. We made the design decision to put in the tile size and the max fish 
per tile as we noticed that
those aspects seemed to be uniform and reusable and made sense to be publicly accessible. So these values are in the constants file in order to not use any
magic numbers.

- Contains game tree source code (game_tree.py). Has all the functionality related to created
a game tree and querying whether an action is legal and applying a function to all child states of
a particular tree node.

- Contains game state source code (state.py). Has all the functionality related to initializing a game 
state, along with placing/moving avatars on behalf of players, determining whether there are any moves left
for any player in the game (is the game over), and rendering the game state. 

- Contains board source code (board.py). Has all the functionality related to initializing a board,
checking if moves are valid, removing a tile, and rendering the board. Unfortunately, the board
depends on the tile as the tile is what declares the tile size and the max num fish per tile. So we
know that there are improved areas for design but had to follow the spec.

- Contains tile source code (tile.py). Has all the functionality related to creating a tile instance
and getter methods for all the attributes, such as num fish per tile.

- Contains tile, fish, and penguin constants source code (tile_fish_penguin_constants.py). These
are constants that detail the tile size, max num fish per tile, the fish size, the penguin size, and 
the penguin colors.

- Contains fish image source code (fish.py). Takes in an x and y base position and has functionality
to draw a fish given a canvas.

- Contains penguin image source code (penguin.py). Takes in an x and y base position and has functionality
to draw a penguin given a canvas.

- Contains board unit tests (board_unit_tests.py). 

- Contains game state unit tests (game_state_unit_tests.py)

- Contains game tree unit tests (game_tree_unit_tests.py)


Sub-Directory Planning:

- This folder contains the planning that goes into constructing the game.

- Contains our thoughts for milestones (milestones.pdf)

- Contains our thoughts for system layout (system.pdf)

- Contains our thoughts for game state data representation (game-state.md)

- Contains my thoughts for a data representation for all games (games.md)

- Contains my thoughts for the API for a player component (player_interface.py)

- Contains my thoughts for the protocol for the API (player_protocol.md)

- Contains my thoughts for the referee component (referee.md)

- **Contains my thoughts for the manager protocol (manager-protocol.md)**
 
***3, 4, 5, 6:***
- Contains our test harness for game board (xboard), game state (xstate), game tree (xtree), and
 strategy (xstrategy) functionality
  - Sub-Directory Tests
    - Contains *-in.json, and *-out.json, where * = 1, 2, or 3. These are the json
    test files used in the test harness.
  - Sub-Directory Other
    - Contains our 3rd party json stream parser (json_stream_parser.py) 
    

             
**Roadmap: How does everything interact?**

Planning: This is the planning part, so it's our ideas in memo form. It relates
to things in Common because Common is what manifests things in Planning, or corrects
and adds functionality.

Common: 
- game_tree.py -> direct downstream interaction with state.py. This is because a game is fed an input state, and a game_tree is a tree of game states.

- state.py -> direct downstream interaction with board.py, fish.py, and penguin.py. This is because a state is composed
of a Board instance, and it requires the fish and penguin images in order to render the game state.

- board.py -> direct downstream interaction with tile.py. This is because a board is composed of tiles. 

- tile_fish_penguin_constants.py -> all files use constants from here in some way.

- game_tree_unit_tests.py -> bring all the game tree functionality together. Makes sure that game tree, game state, and board functionality are working.

- game_state_unit_tests.py -> bring all the game state functionality together. Makes sure that game state and board
functionality are working. 

- board_unit_tests.py -> bring all the board functionality together. Make sure that
the board and tile functionality are working.

Player:

- **player.py -> The implementation of a Player in order to realize the game logic of placement and moving avatars.**
- strategy.py -> Utilizes a GameState and also instantiates a GameTree in order to perform the
placement/choice of move functionality.

- **player_unit_tests.py** -> Brings all the player functionality together. 
- strategy_unit_tests.py -> Brings all the strategy functionality together, and implicitly tests the GameTree and GameState 
methods.

**Admin:
Has components that administer everything in the game. So utilizes all of the different game components in order to keep everything running. The
Referee is in charge of a game, the tournament manager is in charge of a tournament, where there are 
many games running.**


The test harnesses (xboard, xstate, xtree, and xstrategy) make sure that 
 - board, game state, game tree, and strategy functionality are all working 

The Tests folder in each harness directory contains input fed into these harnesses and expected output for them. 

The Other folder in each harness directory contains a JSON stream parser, which parses json input so that we 
can actually do things with the test harness.

**How to run the Test Harness**

Folders and exes per milestone:
 - **Strategy (Folder 6, xstrategy)**
 - Tree (Folder 5, xtree)
 - State (Folder 4, xstate)
 - Board (Folder 3, xboard)
Navigate to the folder for the milestone. There are different ways to run.
   - Run ./x* < Tests/*-in.json | diff - Tests/*-out.json. There should be no diff.      
   - Run ./x*< Tests/*-in.json, to just see the output of x*.
   - Run ./x*. Type in your input to stdin. Press ctrl+d. Then see the x* output. 
             
**How to run the unit tests (xtest script)**

How To Run the Unit Test Suite 

- Navigate to the Fish folder
- Run ./xtest (you'll see messages when it's running each set of unit tests and the results)

How To Run Individual Tests

- **Navigate to the Fish/Admin folder**
- **Run "python3 referee_unit_tests.py TestReferee.<test_case_name>" (or whatever python3 is named on your machine)**
 ---
 - Navigate to the Fish/Player folder
 - **Run "python3 player_unit_tests.py TestPlayer.<test_case_name>" (or whatever python3 is named on your machine)**
 - Run "python3 strategy_unit_tests.py TestStrategy.<test_case_name>" (or whatever python3 is named on your machine)
 ---
 - Navigate to the Fish/Common folder
 - Run "python3 game_tree_unit_tests.py TestGameTree.<test_case_name>" (or whatever python3 is named on your machine)
 - Run "python3 game_state_unit_tests.py TestGameState.<test_case_name>" (or whatever python3 is named on your machine)
 - Run "python3 board_unit_tests.py TestBoard.<test_case_name>" (or whatever python3 is named on your machine)
 
