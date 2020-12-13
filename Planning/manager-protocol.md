I believe that it is the referee's job to deal with the remote players getting disconnected. The referee
will then tell this to the tournament manager, at the end of the game, and the tournament manager will keep track of
who those players are (along with the cheaters).

1. First, some external thing (not sure what because it cannot be a game component)
will instantiate a TournamentManager object, and will pass in a list of all the Players 
who signed up for the tournament. This list will already be ordered by age of the Players, which
either is how long the player has been signed up for, so last to sign up is first in the list, or maybe some birthday communicated in a message
when the Player deals with the sign up server. I think it will most likely be sign-up age as that is what it says in Fish.com a plan, so the player who signed up last will be at the front of the list, etc.
2. Next, the external thing will call the run_tournament method, only once. Since I think the tournament will be run round robin,
meaning every player plays against every other player (good players who don't cheat), the method is kind of like an infinite 
while loop that terminates once every player has played against every other player. So the 'stop' condition will be measured by a function called
is_tournament_over. 
3. So within the while loop in run_tournament, the method create_referee is called first by the manager.
    - Within create_referee
       - the method group_players is called first, once, and returns a List of 2-4 players who have not cheated/failed and who have not played against each other 
to be given to this referee. Then random values are generated, one for the board_rows, and another for the board_columns. 
       - Afterwards, a Referee object is instantiated with the List of players, the board_rows, and the board_columns as parameters.
5. After the Referee object is returned from create_referee, then the Referee's run_game method will be called by the manager.
6. The return value of run_game, which is the game outcome, will be used to update the manager's games_won attribute by adding 1 
to the win_count of each player who won a particular game. So update_win_count is called.
7. Then, the statistics (the leaderboard of top 10 players, see the interface for an explanation) are reported by the manager calling
the report_statistics method.
7. Everything will keep executing in this order until everyone has played everyone.
8. Then, the winner will be reported to tournament observers by the manager calling report_winner.
9. The return value of run_tournament will be the blacklist of cheating players, so that they can
never sign up for another tournament again.

Here is a visualization of the sequence in order:

    run_tournament:
        while tournament_is_not_over:
            create_referee (inside create_referee: call group_players, then instantiate a Referee object)
            referee.run_game 
            update_win_count
            report_statistics
        report_winner
        return blacklist


