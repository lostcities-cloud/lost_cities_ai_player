#!bin/python

import random
import sys
import operator
from lost_cities import *

print "Welcome to computer vs computer Lost Cities." 

# pick strategies.  This interface is poor, but it works for now.
# currently, use expected, expected, simple, simple, 100 To see the
# computer play 100 games against itself with two different strategies
print "Please enter a string which represents player a's play strategy: "
a_play_strat = raw_input()

print "Please enter a string which represents player a's draw strategy: "
a_draw_strat = raw_input()

print "Please enter a string which represents player b's play strategy: "
b_play_strat = raw_input()

print "Please enter a string which represents player b's draw strategy: "
b_draw_strat = raw_input()

print "How many games would you like them to play against each other? "
num_games = int(raw_input())


a_first_wins = 0
b_first_wins = 0
a_last_wins = 0
b_last_wins = 0

ties = 0

a_first_avg_score = 0
b_first_avg_score = 0
a_last_avg_score = 0
b_last_avg_score = 0

for x in range(num_games):
    # Do half of the games with a first player and half with b first
    if x < (num_games/2):
        result = play_game('a', a_play_strat, a_draw_strat,'b', b_play_strat, b_draw_strat)
        result = result.split()
        if result[0] == 'a':
            a_first_wins += 1
        elif result[0] == 't':
            ties += 1
        elif result[0] == 'b':
            b_last_wins += 1

        a_first_avg_score += int(result[1])
        b_last_avg_score += int(result[2])
    else:
        result = play_game('b', b_play_strat, b_draw_strat, 'a', a_play_strat, a_draw_strat)
        result = result.split()
        if result[0] == 'b':
            b_first_wins += 1
        elif result[0] == 't':
            ties += 1
        elif result[0] == 'a':
            a_last_wins += 1

        b_first_avg_score += int(result[1])
        a_last_avg_score += int(result[2])

# Present statistical results
print "Results: Player a won " + str(1.0 * (a_first_wins + a_last_wins) / num_games) + " Player b won " + str(1.0 * (b_first_wins + b_last_wins) / num_games)
print "Ties: " + str(ties)
print "Player a's average score was " + str(1.0 * (a_first_avg_score + a_last_avg_score) / num_games)
print "Player b's average score was " + str(1.0 * (b_first_avg_score + b_last_avg_score) / num_games)
print "When Player a goes first, a wins " + str((2.0 * a_first_wins) / num_games)
print "When Player a goes first, a's average score is " + str((2.0 * a_first_avg_score) / num_games) + " while b's average is " + str((2.0 * b_last_avg_score) / num_games)
print "When Player b goes first, b wins " + str((2.0 * b_first_wins) / num_games)
print "When Player b goes first, b's average score is " + str((2.0 * b_first_avg_score) / num_games) + " while a's average is " + str((2.0 * a_last_avg_score) / num_games)
