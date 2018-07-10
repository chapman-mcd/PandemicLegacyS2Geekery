"""
Define the classes for game execution and typical game variables
"""

from DeckClasses import *

class PandemicGame(object):
    """
    This class represents one playthrough of a Pandemic Legacy Season2 game in order to model the effect of different
    setups for the game decks.  Games will play through the turns and report the status at various intervals.  They will
    also track a couple key events

    The initialization will build an infection deck and a player deck.

    The game will then run a number of "turns". After each "turn", the game will check status.

    After a set condition, the game will "end" and report the final status and variables
    """

    def __init__(self, model_name, game_number, input_inf_deck, input_player_deck, initial_player_draw=8,
                 special_cards={}, searchable_cards={}):
        """
        Initializes the game.  Sets up tracking variables and the decks.
        :param model_name:string, refers to what test is being run
        :param game_number:integer, number of the current game
        :param input_inf_deck:list of cards to be used to generate the infection deck
        :param input_player_deck:dictionary of cards for the player deck.  key, value = card, quantity
        :param initial_player_draw:integer, number of cards in player hands at start of game
        :param special_cards:dictionary. keys are cards to be tracked as 'special'
        :param searchable_cards:dictionary. keys are cards to be tracked as searchable
        """

        # Store all the delicious variables we just got passed
        self.model_name = model_name
        self.game_number = game_number
        self.special_cards = special_cards
        self.searchable_cards = searchable_cards
        self.initial_player_draw = initial_player_draw

        #Create the two decks
        self.infection_deck = InfectionDeck(input_inf_deck)
        self.player_deck = PlayerDeck(input_player_deck)

        # Setup standard game variables
        self.initial_infection_draw = 9
        self.current_infection_level = 0
        self.turn_number = 0
        self.total_cards_drawn = 0

        # Set up tracking variables
        self.searchable_cards_drawn = 0
        self.special_cards_drawn = 0
        self.turns_to_8_cubes_above_pop = None
        # Epidemic timing - a dictionary.  key, value = # of Epidemics, # of turns to draw that number of Epidemics
        # Numbers not reached are None
        self.epidemic_timing = {}
        for i in range(10):
            self.epidemic_timing[i+1] = None
        self.epidemics_drawn = 0
        self.total_cubes_removed_above_pop = 0
        self.cubes_removed_by_city = {}
        self.hollow_men_dropped_by_city = {}
        self.hollow_men_pop_loss_by_city = {}

        for city in self.infection_deck.get_unique_values():
            self.cubes_removed_by_city[city] = 0
            self.hollow_men_dropped_by_city[city] = 0
            self.hollow_men_pop_loss_by_city[city] = 0

        # Set up standard reference variables
        self.infection_rate_lookup = {
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

        #Draw initial cards
        initial_draw = self.player_deck.setup(self.initial_player_draw)

        for card in initial_draw:
            if card in self.searchable_cards:
                self.searchable_cards_drawn += 1
            if card in self.special_cards:
                self.special_cards_drawn += 1

        for i in range(self.initial_infection_draw):
            card = self.infection_deck.draw_top()
            if not card == 'Chicago':
                self.cubes_removed_by_city[card] += 1

    def status_report(self):
        """
        Gives a status report on the game.
        :return: a dictionary with all the critical game data.  keys include, but are not limited to:
            cubes_removed_by_city - dictionary with key, value = city, cubes removed
            hollow_men_dropped_by_city - dictionary with key,value = city, hollow men dropped
            hollow_men_pop_loss_by_city - dictionary with key,value = city, hollow men pop loss
            epidemic_timing - dictionary with key, value = epidemic #, turn drawn.  undrawn epidemics are None.
            total_cubes_removed - integer
            total_cubes_removed_above_pop - integer
            total_hollow_men_dropped - integer
            total_hollow_men_pop_loss - integer
            unique_cities_with_hollow_men - integer
            special_player_cards_drawn - integer
            searchable_player_cards_drawn - integer
            epidemics_drawn - integer
            turns_to_8_cubes_above_pop - integer (None if not reached)
        Void where prohibited.
        """

        report = dict()
        report['cubes_removed_by_city'] = self.cubes_removed_by_city
        report['hollow_men_dropped_by_city'] = self.hollow_men_dropped_by_city
        report['hollow_men_pop_loss_by_city'] = self.hollow_men_pop_loss_by_city
        report['epidemic_timing'] = self.epidemic_timing
        report['total_cubes_removed_above_pop'] = self.total_cubes_removed_above_pop

        # calculate total cubes removed
        temp = 0
        for key in self.cubes_removed_by_city:
            temp += self.cubes_removed_by_city[key]
        report['total_cubes_removed'] = temp

        # calculate total hollow men dropped and unique cities with hollow men
        temp = 0
        uniquetemp = 0
        for key in self.hollow_men_dropped_by_city:
            if self.hollow_men_dropped_by_city[key] > 0:
                temp += self.hollow_men_dropped_by_city[key]
                uniquetemp += 1
        report['total_hollow_men_dropped'] = temp
        report['unique_cities_with_hollow_men'] = uniquetemp

        # calculate total hollow men population loss
        temp = 0
        for key in self.hollow_men_pop_loss_by_city:
            temp += self.hollow_men_pop_loss_by_city[key]
        report['total_hollow_men_pop_loss'] = temp

        report['special_player_cards_drawn'] = self.special_cards_drawn
        report['searchable_player_cards_drawn'] = self.searchable_cards_drawn
        report['epidemics_drawn'] = self.epidemics_drawn
        report['time_to_8_cubes_above_pop'] = self.turns_to_8_cubes_above_pop

        return report

    def track_removed_cubes(self, city):
        """
        Tracks removed cubes, including cubes removed above the # of cards in the infection deck
        :param city: the city card in the infection deck to be removed
        :return: nothing
        """

        # remove the cube
        if not city == 'Chicago':
            self.cubes_removed_by_city[city] += 1

        # check if this puts it above the # of cards in the infection deck
        if self.cubes_removed_by_city[city] > self.infection_deck.get_deck_counts()[city]:
            self.total_cubes_removed_above_pop += 1

        # if this puts us at 8 cubes removed, write down the current turn
        if self.total_cubes_removed_above_pop == 8:
            self.turns_to_8_cubes_above_pop = self.turn_number

    def track_hollow_men_added(self, city):
        """
        Tracks hollow men figures added, including ones that cause population loss.
        :param city: the city cards in the infection deck that needs more hollow men
        :return: nothing
        """

        # add the hollow man
        self.hollow_men_dropped_by_city[city] += 1


        # check if this causes population loss
        # if this is the first one, it causes pop loss
        if self.hollow_men_dropped_by_city[city] == 1:
            self.hollow_men_pop_loss_by_city[city] += 1
        # if this is more than the third, it causes pop loss
        elif self.hollow_men_dropped_by_city[city] > 3:
            self.hollow_men_pop_loss_by_city[city] += 1

    def take_turn(self):
        """
        Takes a pandemic turn:
            Draws and tracks player cards, resolving epidemics.
            Flips infection cards, removinc cubes or adding hollow men as necessary.
        :return: nothing
        """

        self.turn_number += 1
        # draws the two player cards
        for i in range(2):
            self.total_cards_drawn += 1
            # no need to wrap this card draw in a try/catch block.  If this deck is out, then the game is over
            # and the GameOverError should be raised to the game handler.
            card = self.player_deck.draw_top()
            if card == 'Epidemic':
                # Track this
                self.epidemics_drawn +=1
                self.epidemic_timing[self.epidemics_drawn] = self.turn_number
                # Increase
                self.current_infection_level += 1
                # Infect and Intensify
                # wrap in a try block in case we are out of cards.
                try:
                    infectioncard = self.infection_deck.epidemic()
                    # Hollow Men cards are ignored during epidemics, so don't remove cubes if they come up now.
                    if not infectioncard == 'Hollow Men':
                        self.track_removed_cubes(infectioncard)
                # in the extremely rare case that the infection deck is empty when the epidemic is drawn
                # i don't think this scenario is even in the rules - increase infection level by 1 and then shuffle
                # ignoring the draw 1 card in this case
                except GameOverError:
                    self.current_infection_level += 1
                    self.infection_deck.shuffle_discard_on_top()
            if card in self.special_cards:
                self.special_cards_drawn += 1
            if card in self.searchable_cards:
                self.searchable_cards_drawn += 1

        # flips the infection cards
        cards_to_draw = self.infection_rate_lookup[self.current_infection_level]
        hollow_men_inbound = False
        while cards_to_draw > 0:
            # use try in case we are out of cards.
            # if we are out of cards, increase infection rate by 1, shuffle discard on top, and draw again
            try:
                card = self.infection_deck.draw_top()
            except GameOverError:
                self.infection_deck.shuffle_discard_on_top()
                self.current_infection_level += 1
                card = self.infection_deck.draw_top()

            # if the hollow men are inbound, then add a hollow man as long as this is not another hollow men card
            # and set hollow_men_inbound back to false
            if hollow_men_inbound == True:
                if not card == 'Hollow Men':
                    self.track_hollow_men_added(card)
                    hollow_men_inbound = False
                    cards_to_draw += -1
            # if the hollow men are not already in bound
            else:
                # if this is a hollow men card, set them to inbound and continue
                if card == 'Hollow Men':
                    hollow_men_inbound = True
                # if the hollow men are not inbound and this isn't a hollow men card, track the removed cubes
                else:
                    self.track_removed_cubes(card)
                    cards_to_draw += -1



