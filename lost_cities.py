import random
import sys
import operator
from strategy import *
############################################################
# This module sets up a framework for playing lost cities  #
# game of lost cities.                                     #
############################################################

# Card class.  
class card:
    """A simple card class"""
    
    # Value/Color of card
    color = ''
    value = 0
    valid = False

    # Valid colors
    color_list = ['red', 'green', 'white', 'blue', 'yellow']

    # basic functions
    def __init__(self, color, value):
        if type(color) is not str or len(color) == 0:
            print "Color must be a string"
            sys.exit(1)

        if value == "i":
            value = 1
        
        color_valid = self.set_color(color)
        value_valid = self.set_value(value)

        if color_valid and value_valid:
            self.valid = True
    
    def __str__(self):
        if self.value == 1:
            return str(self.color)[0] + "i"
        else:
            return str(self.color)[0] + str(self.value)

    def __repr__(self):
        if self.value == 1:
            return str(self.color)[0] + "i"
        else:
            return str(self.color)[0] + str(self.value)
        
    def __lt__(self, other):
        # return true if self < other
        if (self.color != other.color):
            return self.color < other.color
        
        if (self.color == other.color):
            return self.value < other.value

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__dict__ ==
        other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)
    
    # Set color/value functions.  Checks to make sure card is valid.
    def set_color(self, new_color):
        if type(new_color) is not str:
            print "Color must be a string"
            return False

        if any(new_color == x for x in self.color_list):
            self.color = new_color
            return True
        elif any(new_color == x[0] for x in self.color_list):
            for color in self.color_list:
                if color[0] == new_color:
                    self.color = color
                    return True
        else:
            print "Not a valid color"
            return False

    def is_valid(self):
        return self.valid
        
    def set_value(self, new_value):
        new_value = int(new_value)

        if (new_value > 10 or new_value < 1):
            print "Value must be a 1 (for investment) or 2-10 for a value"
            return False
        else:
            self.value = new_value
            return True
    
    # Take a string of the form "color value" where color is a
    # character and value is a value and update card to the color
    # given by color and value given by value
    def set_card(self, initial_string):
        if type(initial_string) is not str:
            print "Initial string must be a string"
            sys.exit(1)

        card_values = initial_string.split()
        if len(card_values) < 2:
            print "Card initialization did not provide enough fields.  Card initialization failed."
            self.valid = False
            return False
        elif len(card_values) > 2:
            print "Warning, initial string has too many values.  Only using first two."

        color_valid = self.set_color(card_values[0])
        if card_values[1] == 'i' or card_values[1] == 'I':
            value_valid = self.set_value(1)
        else:
            value_valid = self.set_value(card_values[1])
        
        if value_valid and color_valid:
            self.valid = True
        else:
            self.valid = False
        return True


# The board for playing cards
class game_board:
    red_a = []
    red_b = []
    red_discard = []
    
    green_a = []
    green_b = []
    green_discard = []
    
    white_a = []
    white_b = []
    white_discard = []

    blue_a = []
    blue_b = []
    blue_discard = []

    yellow_a = []
    yellow_b = []
    yellow_discard = []

    hand_a = []
    hand_b = []

    discard_a = ""
    discard_b = ""

    a_score = 0
    b_score = 0

    color_list = ['red', 'green', 'white', 'blue', 'yellow']

    # Only need one set, computers don't forget.
    seen_cards = {}

    deck = []

    def __init__(self):
        # Set up deck, shuffle, deal cards
        self.red_a = []
        self.red_b = []
        self.red_discard = []
    
        self.green_a = []
        self.green_b = []
        self.green_discard = []
    
        self.white_a = []
        self.white_b = []
        self.white_discard = []

        self.blue_a = []
        self.blue_b = []
        self.blue_discard = []

        self.yellow_a = []
        self.yellow_b = []
        self.yellow_discard = []

        self.hand_a = []
        self.hand_b = []

        self.discard_a = ""
        self.discard_b = ""

        self.a_score = 0
        self.b_score = 0

        self.deck = []

        self.seen_cards = {}

        self.red_discard.append('-')
        self.blue_discard.append('-')
        self.green_discard.append('-')
        self.white_discard.append('-')
        self.yellow_discard.append('-')

        for color in self.color_list:
            for i in range(10):
                if i+1 == 1:
                    # Three investments
                    c1 = card(color, 1)
                    c2 = card(color, 1)
                    c3 = card(color, 1)
                    self.deck.append(c1)
                    self.deck.append(c2)
                    self.deck.append(c3)
                    self.seen_cards[str(c1)] = 'unseen'
                    self.seen_cards[str(c2)] = 'unseen'
                    self.seen_cards[str(c3)] = 'unseen'
                else:
                    # Once card for all others
                    c = card(color, i+1)
                    self.deck.append(c)
                    self.seen_cards[str(c)] = 'unseen'


        # Shuffle self.deck
        random.shuffle(self.deck)

        # deal hands
        for i in range(8):
            self.hand_a.append(self.deck.pop())
            self.hand_b.append(self.deck.pop())

        
    def __str__(self):
        red_space = 27 - 3 * len(self.red_a)
        red_extra = 0
        green_space = 27 - 3 * len(self.green_a)
        green_extra = 0
        white_space = 27 - 3 * len(self.white_a)
        white_extra = 0
        blue_space = 27 - 3 * len(self.blue_a)
        blue_extra = 0
        yellow_space = 27 - 3 * len(self.yellow_a)
        yellow_extra = 0

        # Get played cards string, need to rewrite using color list
        if len(self.red_a) == 0:
            red_a_str = ""
        else:
            red_extra = 1
            red_a_str = str(sorted(self.red_a, key=lambda cards: cards.value, reverse = True))
            red_a_str = red_a_str[1:-1].translate(None, ',')
    
        if len(self.red_b) == 0:
            red_b_str = ""
        else:
            red_b_str = str(sorted(self.red_b, key = lambda cards: cards.value))
            red_b_str = red_b_str[1:-1].translate(None, ',')

        if len(self.green_a) == 0:
            green_a_str = ""
        else:
            green_extra = 1
            green_a_str = str(sorted(self.green_a, key=lambda cards: cards.value, reverse = True))
            green_a_str = green_a_str[1:-1].translate(None, ',')

        if len(self.green_b) == 0:
            green_b_str = ""
        else:
            green_b_str = str(sorted(self.green_b, key = lambda cards: cards.value))
            green_b_str = green_b_str[1:-1].translate(None, ',')

        if len(self.white_a) == 0:
            white_a_str = ""
        else:
            white_extra = 1
            white_a_str = str(sorted(self.white_a, key=lambda cards: cards.value, reverse = True))
            white_a_str = white_a_str[1:-1].translate(None, ',')

        if len(self.white_b) == 0:
            white_b_str = ""
        else:
            white_b_str = str(sorted(self.white_b, key = lambda cards: cards.value))
            white_b_str = white_b_str[1:-1].translate(None, ',')

        if len(self.blue_a) == 0:
            blue_a_str = ""
        else:
            blue_extra = 1
            blue_a_str = str(sorted(self.blue_a, key=lambda cards: cards.value, reverse = True))
            blue_a_str = blue_a_str[1:-1].translate(None, ',')

        if len(self.blue_b) == 0:
            blue_b_str = ""
        else:
            blue_b_str = str(sorted(self.blue_b, key = lambda cards: cards.value))
            blue_b_str = blue_b_str[1:-1].translate(None, ',')

        if len(self.yellow_a) == 0:
            yellow_a_str = ""
        else:
            yellow_extra = 1
            yellow_a_str = str(sorted(self.yellow_a, key=lambda cards: cards.value, reverse = True))
            yellow_a_str = yellow_a_str[1:-1].translate(None, ',')

        if len(self.yellow_b) == 0:
            yellow_b_str = ""
        else:
            yellow_b_str = str(sorted(self.yellow_b, key = lambda cards: cards.value))
            yellow_b_str = yellow_b_str[1:-1].translate(None, ',')
    
        # Print Board
        self.a_score = self.calc_score('a')
        self.b_score = self.calc_score('b')
        ret_string =  " " * 15 + "Player A" + " " * 12 + "Discard" + " " * 12 + "Player B" 
        ret_string = ret_string + "\nRed:   " + " " * (red_space + red_extra) + red_a_str  
        ret_string = ret_string + " D"+ " " * (2 - len(str(self.red_discard[-1])) / 2) 
        ret_string = ret_string + str(self.red_discard[-1]) 
        ret_string = ret_string + " " * (2 - (len(str(self.red_discard[-1])) - 1) / 2) + "D " +  red_b_str 
        ret_string = ret_string + "\nGreen: " + " " * (green_space + green_extra) + green_a_str  
        ret_string = ret_string + " D"+ " " * (2 - len(str(self.green_discard[-1])) / 2) 
        ret_string = ret_string + str(self.green_discard[-1]) 
        ret_string = ret_string + " " * (2 - (len(str(self.green_discard[-1])) - 1) / 2) + "D " +  green_b_str         
        ret_string = ret_string + "\nWhite: " + " " * (white_space + white_extra) + white_a_str 
        ret_string = ret_string + " D"+ " " * (2 - len(str(self.white_discard[-1])) / 2) 
        ret_string = ret_string + str(self.white_discard[-1]) 
        ret_string = ret_string + " " * (2 - (len(str(self.white_discard[-1])) - 1) / 2) + "D " +  white_b_str 
        ret_string = ret_string + "\nBlue:  " + " " * (blue_space + blue_extra) + blue_a_str
        ret_string = ret_string + " D"+ " " * (2 - len(str(self.blue_discard[-1])) / 2) 
        ret_string = ret_string + str(self.blue_discard[-1]) 
        ret_string = ret_string + " " * (2 - (len(str(self.blue_discard[-1])) - 1) / 2) + "D " +  blue_b_str     
        ret_string = ret_string + "\nYellow:" + " " * (yellow_space + yellow_extra) + yellow_a_str 
        ret_string = ret_string + " D"+ " " * (2 - len(str(self.yellow_discard[-1])) / 2) 
        ret_string = ret_string + str(self.yellow_discard[-1]) 
        ret_string = ret_string + " " * (2 - (len(str(self.yellow_discard[-1])) - 1) / 2) + "D " +  yellow_b_str 
        ret_string = ret_string + "\n--\nPlayer a's score is: " + str(self.a_score)
        ret_string = ret_string + "\nPlayer b's score is: " + str(self.b_score)

        return ret_string
    
    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__dict__ ==
        other.__dict__)

    def __ne__(self, other):
        return not self.__eq__(other)

    # Calculate score/multipliers for a particular color
    def get_color_value(self, player, color):
        played_cards = getattr(self, color + "_" + player)
        
        value = 0
        for played_card in played_cards:
            if (played_card.value != 1):
                value += played_card.value

        return value

    def get_color_multiplier(self, player, color):
        played_cards = getattr(self, color + "_" + player)

        multiplier = 1
        for played_card in played_cards:
            if (played_card.value == 1):
                multiplier += 1

        return multiplier

    def get_color_high_val(self, player, color):
        played_cards = getattr(self, color + "_" + player)
        
        if len(played_cards) != 0:
            played_cards.sort()
            return played_cards[-1].value
        else:
            return 0

    # Calculate score on board
    def calc_score(self, player):
        red_score = 0
        green_score = 0
        white_score = 0
        blue_score = 0
        yellow_score = 0
    
        red_bonus = 0
        green_bonus = 0
        white_bonus = 0
        blue_bonus = 0
        yellow_bonus = 0

        # Need to rewrite this using color_list
        attribute = "red_" + player
        red_cards = getattr(self, attribute)
        multiplier = 1
        if len(red_cards) != 0:
            for c in red_cards:
                if c.value == 1:
                    multiplier += 1
                else:
                    red_score += c.value
            if len(red_cards) >= 8:
                red_bonus = 20
            red_score = (red_score - 20) * multiplier + red_bonus
                
        attribute = "green_" + player
        green_cards = getattr(self, attribute)
        multiplier = 1
        if len(green_cards) != 0:
            for c in green_cards:
                if c.value == 1:
                    multiplier += 1
                else:
                    green_score += c.value
            if len(green_cards) >= 8:
                green_bonus = 20
            green_score = (green_score - 20) * multiplier + green_bonus
            
        attribute = "white_" + player
        white_cards = getattr(self, attribute)
        multiplier = 1
        if len(white_cards) != 0:
            for c in white_cards:
                if c.value == 1:
                    multiplier += 1
                else:
                    white_score += c.value
            if len(white_cards) >= 8:
                white_bonus = 20
            white_score = (white_score - 20) * multiplier + white_bonus

        attribute = "blue_" + player
        blue_cards = getattr(self, attribute)
        multiplier = 1
        if len(blue_cards) != 0:
            for c in blue_cards:
                if c.value == 1:
                    multiplier += 1
                else:
                    blue_score += c.value
            if len(blue_cards) >= 8:
                blue_bonus = 20
            blue_score = (blue_score - 20) * multiplier + blue_bonus

        attribute = "yellow_" + player
        yellow_cards = getattr(self, attribute)
        multiplier = 1
        if len(yellow_cards) != 0:
            for c in yellow_cards:
                if c.value == 1:
                    multiplier += 1
                else:
                    yellow_score += c.value
            if len(yellow_cards) >= 8:
                yellow_bonus = 20
            yellow_score = (yellow_score - 20) * multiplier + yellow_bonus

        return red_score + green_score + white_score + blue_score + yellow_score

    # Updates board with a played card
    def play_card(self, played_card, discard, player):
    # Check if valid player was given
        if player != "a" and player != "b":
            print "Not a valid player"
            sys.exit(1)

        card_found = False
        hand = getattr(self, "hand_" + player)

        # Find and delete card in hand
        count = 0
        while count < len(hand) and not card_found:
            h = hand[count]
            if h == played_card:
                card_found = True
                del hand[count]

            count += 1
        
        ret_val = True
        if card_found:
            if discard:
                # Update discard pile
                (getattr(self, played_card.color + "_discard")).append(played_card)
                # Update seen cards
                self.seen_cards[str(played_card)] = "discard"
                # Set discard color to prevent draw of that color
                setattr(self, "discard_" + player, played_card.color) 
                
            else:
                # Clear discard color
                setattr(self, "discard_" + player, "") 
                
                # Check on validity of play
                cards_on_board = getattr(self, played_card.color + "_" + player);
                if len(cards_on_board) == 0:
                    cards_on_board.append(played_card)
                else:
                    high_val = cards_on_board[-1].value
                    if played_card.value >= high_val:
                        # Update played cards
                        cards_on_board.append(played_card)
                        # Update seen cards
                        self.seen_cards[str(played_card)] = "played"
                    else:
                        ret_val = False
                        print "Not a valid play"
        else:
            ret_val = False
            print "Not a valid play"

        self.a_score = self.calc_score('a')
        self.b_score = self.calc_score('b')

        return ret_val

    def draw_card(self, draw_color, player):
        if len(getattr(self, "hand_" + player))  >= 8:
            print "Hand is already full"
            return False

        color_list = {'red', 'green', 'white', 'blue', 'yellow'}

        valid_color = False
        # Check if color is valid
        for color in color_list:
            if color == draw_color:
                valid_color = True
        
        if valid_color and draw_color != getattr(self, "discard_" + player) and len(getattr(self, draw_color + "_discard")) > 1:
            # Pick card
            draw_card = getattr(self, draw_color + "_discard")[-1]
            # Update discard pile
            del getattr(self, draw_color + "_discard")[-1]
            # Update seen cards
            self.seen_cards[str(draw_card)] = str(player)
        else:
            # Card from deck, not seen
            draw_card = self.deck.pop()

        getattr(self, "hand_" + player).append(draw_card)
        return True

def play_game(player_a, a_play_strat, a_draw_strat, player_b, b_play_strat, b_draw_strat):
    # Initializations
    board = game_board()
    game_not_ended = True
    
    color_list = ["red", "green", "white", "blue", "yellow"]
        
#    print board.deck
    # Deal initial hands

    # Begin Game
    while game_not_ended:
        # Turn loop
        # Do not print out board info to screen
        # Initialize hand a's play values

        if len(board.deck) != 0:
            success = computer_turn('a', board, a_play_strat, a_draw_strat)
        else:
            game_not_ended = False

        if len(board.deck) != 0:
            success = computer_turn('b', board, b_play_strat, b_draw_strat)
        else:
            game_not_ended = False

            
    a_score = board.calc_score('a')
    b_score = board.calc_score('b')
    
    if a_score > b_score:
        return str(player_a) + ' ' + str(a_score) + ' ' + str(b_score)
    elif a_score < b_score:
        return str(player_b) + ' ' + str(a_score) + ' ' + str(b_score)
    else:
        return 't ' + str(a_score) + ' ' + str(b_score)

def computer_turn(player, board, play_strat, draw_strat, suppress_output=True):
    discard = False
    color = ""
    value = -1

    color_list = ["red", "green", "white", "blue", "yellow"]

    play_string = choose_play(board, player, play_strat)

    if not suppress_output:
        print player + "'s play is: " + play_string

    play_list = play_string.split()

    played_card = card('blue', 2)
    
#     print player + " made play " + play_string
#     print str(getattr(board, "hand_" + player))
    print str(board)
        
        # Parse play into string
    if play_list[0] == 'discard':
        discard = True
        color = play_list[1]
        value = int(play_list[2])
        played_card = card(color, value)
    else:
        color = play_list[0]
        value = int(play_list[1])
        played_card = card(color, value)

        # Play card
    success = board.play_card(played_card, discard, player) 

    if not success:
        temp = board.play_card(getattr(board,"hand_" + player), True, player)

    draw_string = choose_draw(board, player, draw_strat)

    if not suppress_output:
        print player + " drew from " + draw_string

    success = success and board.draw_card(draw_string, player)
    return success
