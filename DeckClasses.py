
class PandemicDeck(object):
    '''
    This represents a deck in pandemic, mostly either the player deck or the infection deck.
    All decks have methods to draw off the top and bottom.
    All decks have a draw pile and a "discard" pile.
    
    The deck is a list of strings, each string representing one card in the deck.  Multiple of the same card
    are represented by identical strings in the list.
    '''

    def __init__(self,deck):
        """
        Loads in the deck, and prepares a tuple of the unique values in the deck, and shuffles the draw pile.
        :param deck: a list of strings, representing the cards in the deck.  Multiples of the same card are represented
        by identical strings in the list.
        """
        import random
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

    def get_unique_values(self):
        """
        A programming-course-approved way to get the unique values in the deck.
        :return: a tuple of the unique values in the deck
        """
        return self.unique_values_in_deck

    def drawtop(self):
        """
        Mimics drawing a card off the top of the deck.  Moves the card to the discard pile, and returns the
        string of the card drawn.
        :return: a string representing the card drawn
        """

        card = self.drawpile.pop(0)
        self.discardpile.append(card)
        return card

    def drawbottom(self):
        """
        Mimics drawing a card off the bottom of the deck.  Moves the card to the discard pile, and returns the
        string of the card drawn.
        :return: a string representing the card drawn
        """

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