**Fish** :fish:

I wrote this game for my software development class. 

Fish is a board game for two to four players. 
The game board is a grid of hexagonal tiles, each of which displays a positive number of fish, and it is possible for there to be holes in the board.
The player avatars come in the shape of penguins, which eat fish, and each player is dealt 6-N penguins, where N is the number of players. Each player receives one color for all of its penguins; the different colors are red, white, brown and black. The goal of the game is to collect as many fish as possible. Each game is administered by a Referee that ensures that players are behaving well. 

The game commences with a round-robin placement phase, where players place a penguin on the board one at a time. Once all penguins have been placed, the movement phase comes into effect. When a player takes a turn, it can move a penguin across a boundary of hexagons in a straight line (horizontal, vertical, or diagonal), up to (but not including) a hole or another penguin occupying a tile. A player collects fish after this move has been made–obtaining the number of fish on the tile which it moved *from*, not to. If a player cannot move any of its penguins, it is skipped. 

The game ends when no player can move any of its penguins. The player(s) that collected the most fish win the game. 

Unit tests can be run by running Fish/xtest. 

Though there is no real-time game progress visualization element to this project, a snapshot of a game in a particular state can indeed be rendered visually. Here is what a 4x3  game board looks like for 4 players with a random number of fish per tile, 2 pre-selected holes, and 1 placement round done:



![fish board](https://github.com/eshwaribhide/Fish/blob/master/fish_board.png)


 
