import random
from collections import Counter


class GameOverError(Exception):
    def __init__(self, message):
        super().__init__(message)


class PandemicDeck(object):
    """
    This represents a deck in pandemic, mostly either the player deck or the infection deck.
    All decks have methods to draw off the top and bottom.
    All decks have a draw pile and a "discard" pile.
    
    The deck is a list of strings, each string representing one card in the deck.  Multiple of the same card
    are represented by identical strings in the list.
    """

    def __init__(self, deck):
        """
        Loads in the deck, and prepares a tuple of the unique values in the deck, and shuffles the draw pile.
        :param deck: a list of strings, representing the cards in the deck.  Multiples of the same card are represented
        by identical strings in the list.
        """
        self.deck = deck
        self.drawpile = self.deck
        self.discardpile = []
        # generate a tuple of the unique values in the deck (useful for plotting, etc)
        unique_values_in_deck = []
        for item in deck:
            if item not in unique_values_in_deck:
                unique_values_in_deck.append(item)
        self.unique_values_in_deck = tuple(unique_values_in_deck)
        random.shuffle(self.drawpile)

        # generate a dictionary with the number of each card in the infection deck
        self.deck_counts = Counter(self.deck)

    def get_unique_values(self):
        """
        A programming-course-approved way to get the unique values in the deck.
        :return: a tuple of the unique values in the deck
        """
        return self.unique_values_in_deck

    def get_deck_counts(self):
        """
        A programming-course-approved way to get the amount of each card in the deck.
        :return: a dictionary with keys=cards and values=quantity of cards
        """
        return self.deck_counts

    def draw_top(self):
        """
        Mimics drawing a card off the top of the deck.  Moves the card to the discard pile, and returns the
        string of the card drawn.  Raises GameOverError if there are no cards.
        :return: a string representing the card drawn
        """

        if len(self.drawpile) == 0:
            raise GameOverError("GAME OVER MAN.  GAME OVER.")
        card = self.drawpile.pop(0)
        self.discardpile.append(card)
        return card

    def draw_bottom(self):
        """
        Mimics drawing a card off the bottom of the deck.  Moves the card to the discard pile, and returns the
        string of the card drawn.  Raises GameOverError if there are no cards.
        :return: a string representing the card drawn
        """
        if len(self.drawpile) == 0:
            raise GameOverError("GAME OVER MAN.  GAME OVER.")
        card = self.drawpile.pop()
        self.discardpile.append(card)
        return card

    def shuffle_discard_on_top(self):
        """
        Shuffles the discard pile and puts it on top of the deck.  Like what happens when an epidemic is drawn.
        :return: nothing
        """

        random.shuffle(self.discardpile)
        self.drawpile = self.discardpile + self.drawpile

    def discard_specific(self, card):
        """
        Pulls one instance of a specific card out of the draw and into the discard pile.
        :return: nothing
        """

        if card in self.drawpile:
            self.drawpile.pop(self.drawpile.index(card))
            self.discardpile.append(card)

    def discard_all_specific(self, card):
        """
        Discards all of a specific card from the draw into the discard pile
        :param card: a card in the pile
        :return: nothing
        """

        while card in self.drawpile:
            self.discard_specific(card)


class InfectionDeck(PandemicDeck):
    """
    This subclass of pandemic deck represents the infection deck.  Setup is a bit unique, but otherwise its the same
    """
    def __init__(self, deck):
        super(InfectionDeck, self).__init__(deck)
        # infectiondeck specific setup.  Put all hollow men cards in the discard pile, then shuffle the draw pile
        self.discard_all_specific("Hollow Men")
        random.shuffle(self.drawpile)

    def epidemic(self):
        """
        This takes all the actions required for an epidemic.  Draws a card off the bottom, then shuffles the
        discard pile onto the draw pile
        :return: the card off the bottom
        """
        card = self.draw_bottom()
        self.shuffle_discard_on_top()
        return card


class PlayerDeck(PandemicDeck):
    """
    This represents the pandemic player deck.  This will use fewer of the parent class elements and have to 
    override more of them.
    """
    def __init__(self, deck):
        """
        Initializes the player deck.  Populates the decks, but does not initialize.  Must use setup method.
        :param deck: a dictionary.  key,value pairs are cardname, quantity.
        """
        self.deck = deck
        self.drawpile = []
        self.discardpile = []
        # build the deck and shuffle the non-epidemic cards
        for item in deck:
            if item.lower() == 'epidemic':
                self.epidemics = ['Epidemic'] * int(deck[item])
            else:
                self.drawpile += [item] * int(deck[item])
        random.shuffle(self.drawpile)
        # generate a tuple of the unique values in the deck (useful for plotting, etc)
        unique_values_in_deck = []
        for item in deck:
            if item not in unique_values_in_deck:
                unique_values_in_deck.append(item)
        self.unique_values_in_deck = tuple(unique_values_in_deck)

        # generate a dictionary with the number of each card in the infection deck
        # in this case, that was passed in so just store it.
        self.deck_counts = self.deck

    def setup(self, num_cards_at_start):
        """
        Sets up the deck and puts epidemics in their places.
        :param num_cards_at_start: number of cards in player hands at the start of the game.
        :return: a list containing the cards drawn at the start
        """
        self.num_cards_at_start = num_cards_at_start

        cards = []
        for i in range(num_cards_at_start):
            cards.append(self.draw_top())

        # easiest way to build the drawpile is the same way it's done in the real game.  divide and shuffle.
        non_epidemic_cards_in_deck = len(self.drawpile)
        num_epidemics = len(self.epidemics)

        # calculate small phase length (floor of the card division) and the number of longer phase (remainder)
        small_phase_length = non_epidemic_cards_in_deck // num_epidemics
        num_larger_phases = non_epidemic_cards_in_deck % num_epidemics

        # initialize a temporary draw pile, and loop through the number of epidemics
        tempdrawpile = []
        for i in range(num_epidemics):
            # create a pile for this shuffle
            this_phase_cards = []

            # determine how many non-epidemic cards should be in it
            if i < num_larger_phases:
                non_epidemics_this_phase = small_phase_length + 1
            else:
                non_epidemics_this_phase = small_phase_length

            # draw cards off the top of the pile to fill this phase
            for z in range(non_epidemics_this_phase):
                this_phase_cards.append(self.draw_top())

            # add the epidemic, shuffle, and add to the back of the draw pile
            this_phase_cards.append('Epidemic')
            random.shuffle(this_phase_cards)
            tempdrawpile += this_phase_cards

        # if there are any cards left in the draw pile at this point, then the math is off somehow
        if len(self.drawpile) > 0:
            raise Exception("You didn't put all the cards in the deck, dummy.")

        # replace the official draw pile with the temp drawpile
        # also replace the discard pile, since using the draw card method put those cards in the discard pile.
        self.drawpile = tempdrawpile
        self.discardpile = cards

        # send back the cards in player hands at start
        return cards
