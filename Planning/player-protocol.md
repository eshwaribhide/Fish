**Purpose: The purpose of a player protocol is to answer two questions: _how_ do I do something, and
_when_ can that thing be done?**

**Who is Using This Protocol? Referees and players.**

**Protocol**
- Step 1: The referee needs to call game_started() to tell a player that the game has started and also their penguin color. This
is only done once.

- Step 2: If Step 1 has already been done, don't go back to it. Now, if the placement phase isn't over, and it is this player's
turn, then the referee should call place_avatar() method. 

- Step 3: If the placement phase is over, and it is this player's turn, then the referee should call placement_phase_is_over().

- Step 4: Assuming the placement phase is over, and it is this player's turn, the referee should call move_avatar().

- Step 5: Once the game is over, the referee should signal this to the player through calling game_is_over().
