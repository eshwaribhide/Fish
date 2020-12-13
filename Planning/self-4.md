## Self-Evaluation Form for Milestone 4

Under each of the following elements below, indicate below where your
TAs can find:

- the interpretation of your data representation for `board`

  - Here, you can see all the data definitions: https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/board.py#L5-L58

  - Though these lines are already included in the permalink above, you can see https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/board.py#L55-L58 for a more detailed data definition for the tiles.

- the interpretation of your data representation for `game state`

  - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/state.py#L6-L78

  - I understand that this can be made more concise; this is something that I will definitely try to do in the future.


- the publicly visible methods/functions for game treees 

  - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/game_tree.py#L50-L95

  - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/game_tree.py#L146-L230

  - Some of the publicly visible functions were not explicitly described in the spec. I made them public because I believed there would be a use for players and referees to use them. For example, to determine the end of the tree, to advance the generator, and useful function objects that could be passed into the apply_to_all_children() method.

- the data description of the game tree, including an interpretation;
  - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/game_tree.py#L3-L48


- a signature/purpose statement of functionality for the first query function
  - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/game_tree.py#L146-L154


- unit tests for first query functionality
  - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish/Common/game_tree_unit_tests.py#L97-L129

**Please use GitHub perma-links to the range of lines in specific
file or a collection of files for each of the above bullet points.**

  WARNING: all perma-links must point to your commit "8d7da63bafb3a2d862ec72dbcc29b641041dae51".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/bayview/tree/8d7da63bafb3a2d862ec72dbcc29b641041dae51/Fish>

