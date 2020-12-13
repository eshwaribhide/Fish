## Self-Evaluation Form for Milestone 2

A fundamental guideline of Fundamentals I, II, and OOD is to design
methods and functions systematically, starting with a signature, a
clear purpose statement (possibly illustrated with examples), and
unit tests.

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of tiles, including an interpretation:
   - <https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/tile.py>
   - This is our file to represent a tile. In this file, we have a clear data description that says this is our representation
  of a tile, we use a class to implement it and have class level and private error-checking/getter functions. We explain the   num_fish_per_tile arg   passed in to the tile in our data description. Size and max fish are self-explanatory
  attributes, then we have an "is_visible" attribute, which we explain. 

- the data description of boards, include an interpretation:
   - <https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py>
   - This is our file to represent the Board. In this file, we have a clear data description that says this is our representation of the board and we used a class to implement it. We describe the various attributes of the board and then our constructor along with all public and private functionality is all contained within this file. 

- the functionality for removing a tile:
  - purpose: 
     - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L237
  - signature: 
     - <https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L236> is the actual signature
     - <https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L238-L239> describes a bit more about the args
  
  - unit tests:
     - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board_unit_tests.py#L160-L180
     - These are explicit tests for the tile removal functionality that also test the different edge cases if a tile cannot be removed

- the functiinality for reaching other tiles on the board:
  - purpose:
     - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L187-L190 is for our main tile reachability checker function
  
  
     - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L157
  is for our helper tile reachability checker function
  
  - signature:
     - For our main tile reachability checker function (official signature along with args descriptions):
       - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L186
       - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L191-L192
    
      - For our helper tile reachability checker function (official signature along with args descriptions)
        - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L158
        - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board.py#L159-L163
 
  - unit tests:
     - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish/Common/board_unit_tests.py#L129-L158
     - These are explicit tests that handle edge cases for when you try to determine reachability from an empty tile or
   out of bounds and also tests general reachability functionality

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "b2a1683760d301b8dc6fbddde9ea1bf3c9a29982".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/bayview/tree/b2a1683760d301b8dc6fbddde9ea1bf3c9a29982/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.
