def choose_play(board, player, strategy):
    # Start with a "simple" strategy
    if strategy == "simple":
        # A simple strategy.  Play card from color with most points
        # GREATER than 0.  Otherwise, discard card
        # of color of smallest value
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

def choose_draw(board, player, strategy):
# Start with a "simple" strategy
    if strategy == "simple":
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
