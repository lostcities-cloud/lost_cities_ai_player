##################################################################
# This file contains strategies.  Currently the interface to these
# functions is achieved by additing to the if-statements in the
# choose_play and choose_draw function.  A string is used to access
# the appropriate strategy.
##################################################################

# A description of the board methods which can be used for these functions:
# board variables:
# 
# $color_$player: Gives the $color cards $player (a or b) has played
#
# $color_discard: Gives the $color cards in discard pile.  The last
# card is the top of the pile
#
# hand_$player: Stores the hand of $player (a or b).  The strategy
# module should only access the current players hand, otherwise the
# strategy is engaging in cheating.
#
# discard_$player: If $player last play was discard, keeps the
# color. The strategy module may only look at the top card, otherwise
# the strategy is involved in cheating.
#
# $player_score: Current score of $player
#
# color_list: Contains a list of card colors
#
# deck: Contains the cards in the deck.  The last card is on top of deck.
#
#
# board methods:
#
# __init__: Initializes board.  In particular, it creates a deck of
# cards, shuffles it and deals 8 cards to each hand.
#
# get_color_value(player, color): Returns face value of $color cards
# played by $player (no investments)
#
# get_color_multiplier(player, color): Returns number of played
# multipliers for $player on $color
#
# get_color_high_val(player, color): Returns highest played value for
# $color and $player
#
# calc_score(player): Calculates the score for $player, updates
# $player_score (other functions, such as play_card, may also update
# score)
#
# len(board.deck): Returns length of deck.
#
# board.$color_discard[-1] Returns top card in $color's discard pile.


# Choose Play
#
# INPUT: board: Current state of game
#        player: Player whose turn we are deciding
#        strategy: string which indicates which strategy to use in making decision
#
# OUTPUT: card_string.  A string of format "discard $color $value" or "$color $value"

import lost_cities as lc

def choose_play(board, player, strategy):
    # Start with a "simple" strategy
    if strategy == "simple":
        card_string = simple_play(board, player)
    elif strategy == "expected":
        card_string = expected_play(board, player)

    return card_string

# A simple play strategy
# Threshold based
# INPUT: board: Current state of game
#        player: Player whose turn we are deciding
#
# OUTPUT: A string of the formate "discard $color $value" or "$color $value"
def simple_play(board, player):
    # A simple strategy.  Play card from color with most points
    # GREATER than 0.  Otherwise, discard smallest card of color of
    # smallest value
    color_list = board.color_list
    color_values = {'red': 0, 'green': 0, 'white': 0, 'blue': 0, 'yellow': 0}
    color_high_val = {'red': 0, 'green': 0, 'white': 0, 'blue': 0, 'yellow': 0}
    color_hand_values = {'red': 0, 'green': 0, 'white': 0, 'blue': 0, 'yellow': 0}
    hand_by_colors = {'red': [], 'green': [], 'white': [], 'blue': [], 'yellow': []}
    min_invalid_card = []
    hand = getattr(board, "hand_" + player)
    hand = sorted(hand)
        
    # First calculate the base value of each color 
    for color in color_list:
        color_values[color] = board.get_color_value(player, color)
        color_high_val[color] = board.get_color_high_val(player, color)
        
    # Calculate the potential worth of cards in hand
    # Keep track of smallest invalid card
    # Update color list to only contain colors in han
    for h in hand:
        color = h.color
        hand_by_colors[color].append(h)
        if h.value >= color_high_val[color]:
            color_hand_values[color] += h.value
        else:
            if len(min_invalid_card) == 0:
                min_invalid_card.append(h)
            elif h.value < min_invalid_card[0].value:
                min_invalid_card[0] = h

    # Note that, 10 is the highest possible value
    min_card_over_threshold_value = 11
    min_playable_card_value = 11

    min_card_over_threshold = 0
    min_playable_card = 0

    # Find value of color in hand.  Keep track of minimum card
    # over threshold.  This card is the card that will be played.
    for color in color_list:
        card_list = hand_by_colors[color]
        for c in card_list:
            # value = 1
#             if card_str[1] != 'i':
#                 value = int(card_str[1,:])

#             c = lc.card(card_str[0], value)
            print color + " " + player
            print color_values[color] + color_hand_values[color]
            if (color_values[color] + color_hand_values[color]) >= 20:
                if c.value < min_card_over_threshold_value and c.value >= color_high_val[color]:
                    min_card_over_threshold = c
                    min_card_over_threshold_value = c.value
           
            if c.value < min_playable_card_value:
                min_playable_card = c
                min_playable_card_value = c.value
            
    # Produce card string
    card_string = ""
    if min_card_over_threshold_value != 11:
        card_string = min_card_over_threshold.color + " " + str(min_card_over_threshold.value)
    elif len(min_invalid_card) != 0:
        card_string = "discard " + min_invalid_card[0].color + " " + str(min_invalid_card[0].value)
    else:
        card_string = "discard " + min_playable_card.color + " " + str(min_playable_card.value)

    return card_string


###

def expected_play(board, player):
    # Strategy which values colors/discard based on expected values of
    # colors.  Still thresholded whether to play or discard
    
    hand = getattr(board, "hand_" + player)
    hand = sorted(hand)

    card_values = {}

    for c in hand:
        card_values[str(c)] = expected_value(c, board, player)

    max_card = lc.card("blue",1)
    max = -1000
    min_card = lc.card("blue",1)
    min = 1000
    # print "Player " + player + "'s card values: " + str(card_values)
    for c in card_values:
        if card_values[c] > max:
            max = card_values[c]
            value = 1
            if c[1] != 'i':
                value = int(c[1:])

            max_card = lc.card(c[0], value)

        if card_values[c] < min:
            min = card_values[c]
            value = 1
            if c[1] != 'i':
                value = int(c[1:])

            min_card = lc.card(c[0], value)

    if max < 0:
        return "discard " + min_card.color + " " + str(min_card.value)
    else:
        return max_card.color + " " + str(max_card.value)
###

def expected_value(play_card, board, player):
    # This function gives the expected value of cards above the given
    # card value assuming that all cards can be played.  Note that
    # this value is only calculating future plays.  i.e. before a card
    # is played on a color, the value is -20 + sum(values *
    # prob. you'll get card).  This ignores the > 8 cardbonus as well.

    # It should be noted that this is actually a weighting of cards
    # which is intended to be approximately the expected value.  In
    # particular, other player's actions are not modeled in much detail
    
    # Check if card is playable
    high_val = board.get_color_high_val(player, play_card.color)
    if play_card.value < high_val:
        return -81

    # Make a list of all cards above the value
    card_list = {}
    for i in range(10):
        c = lc.card(play_card.color, i+1)
        if i+1 >= play_card.value:
            if i+1 == 1:
                # Aggregated weighting for investments
                card_list[str(c)] = 1.5
            else:
                card_list[str(c)] = 0.5
    
    
    # Now go through the player's hand
    hand = getattr(board, "hand_" + player)
    
    for c in hand:
        if str(c) in card_list:
            if c.value == 1:
                card_list[str(c)] += 0.5
            else:
                card_list[str(c)] = 1.0

    enemy_pile = []
    if player != 'a':
        enemy_pile = getattr(board, play_card.color + "_a")
        enemy = 'a'
    elif player != 'b':
        enemy_pile = getattr(board, play_card.color + "_b")
        enemy = 'b'
    else:
        print "Player variable is not a or b."
        return -90

    for c in enemy_pile:
        if str(c) in card_list:
            if c.value == 1:
                card_list[str(c)] += -0.5
            else:
                card_list[str(c)] = 0

    # Check through discard pile, note that the exponential fall-off
    # is a crude approximation
    discard_pile = getattr(board, play_card.color + "_discard")
    
    count = 0
    for c in discard_pile:
        if str(c) in card_list:
            if c.value == 1:
                # combined investment weighting
                card_list[str(c)] += (0.5)**(count) - 0.5
            else:    
                card_list[str(c)] = (0.5)**(count)
        count += 1

    # Check about seen cards
    seen_pile = board.seen_cards
    for c in seen_pile:
        if str(c) in card_list:
            if seen_pile[c] == enemy:
                # Note, this isn't quite accurate, c could be
                # discarded by the other player, though it is unlikely
                card_list[str(c)] = 0

    # Adjustment by cards lower that haven't been played, but could
    # be. Region is commented because test show this does not work as
    # coded. I think it may just need some adjustments, but the
    # current strategy discounts too much.  Needs to be done by
    # estimating likelihood of getting each card...which I am
    # currently estimating, whereas it needs to be done by calculating.
    opportunity_cost = 0
#     for card_str in card_list:
#         value = 1
#         if card_str[1] != 'i':
#             value = int(card_str[1:])
        
#         if value > high_val and value < play_card.value:
#             opportunity_cost -= value * card_list[card_str]

    # Now, add up score, find 
    cost_to_be_paid = 0
    investments = 0
    if play_card.value > 1:
        investments = board.get_color_multiplier(player, play_card.color)
    else:
        investments = (board.get_color_multiplier(player, play_card.color) - 1.0) * 0.5 + card_list[str(lc.card(play_card.color, 1))] + 1.0

    gains_to_be_made = 0
    
    if board.get_color_high_val(player, play_card.color) == 0:
        cost_to_be_paid = -20
    
    for card_string in card_list:
        
        value = 1
        if card_string[1] != 'i':
            value = int(card_string[1:])

        c = lc.card(card_string[0], value)
        if c.value != 1:
            gains_to_be_made += card_list[str(c)] * c.value

    return (cost_to_be_paid + gains_to_be_made + opportunity_cost) * investments


# Choose draw
# INPUT: board: is the current state of the game.  
#        player: is the player to decide on a draw.
#        strategy: is a string which determines the strategy to use to make this decision.
#
# OUTPUT: draw_string, a string of the format "deck" or "$color", indicates draw.
def choose_draw(board, player, strategy):
# Start with a "simple" strategy
    if strategy == "simple" or strategy == "expected":
        draw_string = simple_draw(board, player)

    return draw_string

def simple_draw(board, player):
    # Simple draw
    color_list = board.color_list
    
#     for color in color_list:
#         discard_cards = getattr(board, color + "_" + discard)
#         discard_card = discard_cards[-1]
#         played_cards = getattr(board, color + "_" + player)
#         if board.get_color_high_val(player, color) <= discard_card.value or len(played_cards) == 0:
            
    # A simple strategy. 
    color_list = board.color_list
    color_values = {'red': 0, 'green': 0, 'white': 0, 'blue': 0, 'yellow': 0}
    color_multipliers = {'red': 1, 'green': 1, 'white': 1, 'blue': 1, 'yellow': 1}
    color_high_val = {'red': 0, 'green': 0, 'white': 0, 'blue': 0, 'yellow': 0}
    color_hand_values = {'red': 0, 'green': 0, 'white': 0, 'blue': 0, 'yellow': 0}
    hand_by_colors = {'red': [], 'green': [], 'white': [], 'blue': [], 'yellow': []}
    hand = getattr(board, "hand_" + player)
    hand = sorted(hand)
        
    discard_color = getattr(board, "discard_" + player)

    # First calculate the base value of each color 
    for color in color_list:
        color_values[color] = board.get_color_value(player, color)
        color_multipliers[color] = board.get_color_multiplier(player, color)
        color_high_val[color] = board.get_color_high_val(player, color)
        
    # Calculate the potential worth of cards in hand
    # Keep track of smallest invalid card
    # Update color list to colors in hand
    color_list = []
    for h in hand:
        color = h.color
        hand_by_colors[color].append(h)
        if len(hand_by_colors[color]) == 1:
            color_list.append(color)
        if h.value >= color_high_val[color]:
            color_hand_values[color] += h.value
        
    max_value = 0
    max_color = ""
    # Find color that has maximum value in hand/on board AND has a
    # valid card on the top of the discard pile
        
    for color in color_list:
        discard_pile = getattr(board, color + "_discard")
        if len(discard_pile) > 1: 
            if discard_color != color and discard_pile[-1].value >= color_high_val[color]:
                if color_multipliers[color] * (color_hand_values[color] + color_values[color] + discard_pile[-1].value - 20) > max_value:
                    max_value = color_multipliers[color] * (color_hand_values[color] + color_values[color] + discard_pile[-1].value)
                    max_color = color

    # Produce draw string
    draw_string = "deck"
    if max_value > 0:
        draw_string = max_color
        
    return draw_string

###


