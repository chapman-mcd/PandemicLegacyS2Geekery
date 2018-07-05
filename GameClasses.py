"""
Define the classes for game execution and typical game variables
"""

import DeckClasses

class PandemicGame(object):
    '''
    This class represents one playthrough of a Pandemic Legacy Season2 game in order to model the effect of different
    setups for the game decks.  Games will play through the turns and report the status at various intervals.  They will
    also track a couple key events

    The initialization will build an infection deck and a player deck.

    The game will then run a number of "turns". After each "turn", the game will check status.

    After a set condition, the game will "end" and report the final status and variables
    '''

    def __init__(self,model_name,game_number,input_inf_deck,input_player_deck):
        '''
        :param model_name: the name used when printing reports
        :param game_number: the number used when printing reports
        :param input_inf_deck: the cards to be used in the infection deck
        :param input_player_deck: the cards to be used in the player deck

        Set variables that will be needed throughout the game and for reporting.
        Then initialize the two decks and perform the start of game setup
        '''
        mode_name = model_name
        game_number = game_number

        #Setup standard game variables
        infection_rate = {
            0: 2,
            1: 2,
            2: 2,
            3: 3,
            4: 3,
            5: 4,
            6: 4,
            7: 5,
            8: 5,
            9: 5,
            10: 5
        }

        num_of_epidemics = {
            30: 5,
            31: 5,
            32: 5,
            33: 5,
            34: 5,
            35: 5,
            36: 5,
            37: 6,
            38: 6,
            39: 6,
            40: 6,
            41: 6,
            42: 6,
            43: 6,
            44: 6,
            45: 7,
            46: 7,
            47: 7,
            48: 7,
            49: 7,
            50: 7,
            51: 7,
            52: 8,
            53: 8,
            54: 8,
            55: 8,
            56: 8,
            57: 8,
            58: 9,
            59: 9,
            60: 9,
            61: 9,
            62: 9,
            63: 10,
            64: 10,
            65: 10,
            66: 10,
            67: 10,
            68: 10,
            69: 10,
            70: 10,
            71: 10,
            72: 10,
            73: 10,
            74: 10,
            75: 10,
            76: 10
        }
        epidemics_drawn = 0

        initial_infection_draw = 9
        initial_player_draw = 8

        turns_to_report = [5, 10, 15, 20, 25, 30, 35]

        list_of_cities = [
            'new york',
            'washington',
            'london',
            'chicago',
            'denver',
            'san francisco',
            'atlanta',
            'paris',
            'st petersburg',
            'johannesburg',
            'sao paolo',
            'jacksonville',
            'lagos',
            'mexico city',
            'los angeles',
            'buenos aires',
            'bogota',
            'santiago',
            'lima',
            'dar es salaam',
            'istanbul',
            'tripoli',
            'antanarivo',
            'moscow',
            'baghdad'
        ]

        #Create the two decks
        infection_deck = PandemicDeck(input_inf_deck)
        number_of_epidemics = len(input_player_deck)
        player_deck = PandemicDeck(input_player_deck)

        #Draw initial cards
        for i in range(initial_player_draw):
            player_deck.drawtop()

        for i in range(initial_infection_draw):
            infection_deck.drawtop()

    def end_turn(self):
        '''
        At the end of each turn, two player cards get drawn, then draw infection cards up to the infection fate
        return the number of player cards remaining
        '''

        for i in ranage(2):
            card = player_deck.drawtop()
            if card = 'epidemic':
                #Increase
                epidemics_drawn += 1
                #Infect
                infection_deck.drawbottom()
                #Intensify
                infection_deck.shuffle_discard_on_top()

        keep_cards = 0
        while keep_cards < range(infection_rate[epidemics_drawn]):
            card = infection_deck.drawtop()
            if card != 'hollow men':
                keep_card += 1



