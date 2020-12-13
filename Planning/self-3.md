## Self-Evaluation Form for Milestone 3

Under each of the following elements below, indicate below where your
TAs can find:

- the data description of states, including an interpretation:

    - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/fd0030ebaeca1b9b19c3179a69071c2db7e49f48/Fish/Common/state.py#L27-L74
    - I explicity give the data description, and I have comments for each of the fields which give more information about them in terms of their data type and interpretation.

- a signature/purpose statement of functionality that creates states 

   - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/fd0030ebaeca1b9b19c3179a69071c2db7e49f48/Fish/Common/state.py#L16-L97
   - I don't have an explicit function to create it: I just have a class create a state. In terms of the signature, you can see comments for each of the class fields to see their data type. Purpose statement is explicit at the top.

- unit tests for functionality of taking a turn 
   - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/fd0030ebaeca1b9b19c3179a69071c2db7e49f48/Fish/Common/game_state_unit_tests.py#L100-L117
   - Implicitly showing that player 1 needs to do the placement first, then player 2. 

- unit tests for functionality of placing an avatar 

   - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/fd0030ebaeca1b9b19c3179a69071c2db7e49f48/Fish/Common/game_state_unit_tests.py#L68-L98
   - This is an explicit test for avatar placement.

- unit tests for functionality of final-state test

   - https://github.ccs.neu.edu/CS4500-F20/bayview/blob/fd0030ebaeca1b9b19c3179a69071c2db7e49f48/Fish/Common/game_state_unit_tests.py#L137-L208
   - These two tests play out a game, making sure that the game is registered as over when there's nothing left and NOT registered as over before that.

The ideal feedback is a GitHub perma-link to the range of lines in specific
file or a collection of files for each of the above bullet points.

  WARNING: all such links must point to your commit "fd0030ebaeca1b9b19c3179a69071c2db7e49f48".
  Any bad links will result in a zero score for this self-evaluation.
  Here is an example link:
    <https://github.ccs.neu.edu/CS4500-F20/bayview/tree/fd0030ebaeca1b9b19c3179a69071c2db7e49f48/Fish>

A lesser alternative is to specify paths to files and, if files are
longer than a laptop screen, positions within files are appropriate
responses.

In either case you may wish to, beneath each snippet of code you
indicate, add a line or two of commentary that explains how you think
the specified code snippets answers the request.

## Partnership Eval 

Select ONE of the following choices by deleting the other two options.

**N/A. I do not have a partner.**

If you chose C, please give some further explanation below describing
the state of your partnership and whether and how you have been or are
addressing this disparity. Describe the overall trajectory of your
partnership from the beginning until now. Be honest with your answer
here, and with each other. Even if it's uncomfortable reading this
together right now.

If you chose one of the other two options, you should feel free to
also add some explanation if you wish. 
