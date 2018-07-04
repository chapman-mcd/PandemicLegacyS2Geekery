import random

######################################################
# Input Information
######################################################

infection_rate = {
    0:2,
    1:2,
    2:2,
    3:3,
    4:3,
    5:4,
    6:4,
    7:5,
    8:5,
    9:5,
    10:5
    }

num_of_epidemics = {
    30:5,
    31:5,
    32:5,
    33:5,
    34:5,
    35:5,
    36:5,
    37:6,
    38:6,
    39:6,
    40:6,
    41:6,
    42:6,
    43:6,
    44:6,
    45:7,
    46:7,
    47:7,
    48:7,
    49:7,
    50:7,
    51:7,
    52:8,
    53:8,
    54:8,
    55:8,
    56:8,
    57:8,
    58:9,
    59:9,
    60:9,
    61:9,
    62:9,
    63:10,
    64:10,
    65:10,
    66:10,
    67:10,
    68:10,
    69:10,
    70:10,
    71:10,
    72:10,
    73:10,
    74:10,
    75:10,
    76:10
    }

## TODO: turn into a variable value
#cards_per_epidemic = 6

initial_draw = 9 #infection draw
initial_player_cards = 8 # num of players times 2

turns_to_simulate = 20

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

infection_cities = {
    'new york': 3,
    'washington': 3,
    'london': 3,
    'chicago': 2,
    'denver': 2,
    'san francisco': 2,
    'atlanta': 1,
    'paris': 2,
    'st petersburg': 1,
    'johannesburg': 2,
    'sao paolo': 3,
    'jacksonville': 3,
    'lagos': 3,
    'mexico city': 1,
    'los angeles': 1,
    'buenos aires': 2,
    'bogota': 0,
    'santiago': 1,
    'lima': 1,
    'dar es salaam': 2,
    'istanbul': 3,
    'tripoli': 3,
    'antanarivo': 2,
    'moscow': 1,
    'baghdad': 2
    }

infection_non_cities = {
    'hollow men': 4
    }

draw_contents = {
    'upgrade_city': 9,
    'normal_city': 46,
    'non-city': 13
    }

total_epidemics = num_of_epidemics[draw_contents['upgrade_city'] + draw_contents['normal_city']]


######################################################
# Setup the Decks
######################################################

draw_deck = []
cubes_lost = {}
hollow_men_added = {}
population_lost = {}

for city,num_cards in infection_cities.items():

    #Set initial values
    cubes_lost[city] = 0
    hollow_men_added[city] = 0
    population_lost[city] = 0

    while num_cards > 0:
        draw_deck.append(city)
        num_cards -= 1

print(draw_deck)

random.shuffle(draw_deck)

print(draw_deck)

discard_deck = []

for city,num_cards in infection_non_cities.items():
    while num_cards > 0:
        discard_deck.append(city)
        num_cards -= 1

print(discard_deck)

player_deck = []
init_player_deck = []
upgrades_found = 0
player_drawn = 0
epidemic_count = 0

for card,num_cards in draw_contents.items():
    while num_cards > 0:
        init_player_deck.append(card)
        num_cards -= 1

player_discard = []
random.shuffle(init_player_deck)

temp_draw = 0

while temp_draw < initial_player_cards:
    player_discard.append(init_player_deck.pop())
    temp_draw +=1

temp_epidemic_count = 1

cards_per_epidemic = len(init_player_deck) // total_epidemics

while temp_epidemic_count < total_epidemics:
    cards_drawn = 0
    player_deck_substack = ['epidemic']
    while cards_drawn < cards_per_epidemic:
        player_deck_substack.append(init_player_deck.pop())
        cards_drawn += 1

    random.shuffle(player_deck_substack)
    player_deck = player_deck + player_deck_substack
    temp_epidemic_count += 1

init_player_deck.append('epidemic')
random.shuffle(init_player_deck)
player_deck = player_deck + init_player_deck

print(player_deck)
print(player_discard)


######################################################
# Initial Infection
######################################################

def drawCards(num_cards):

    cards_drawn = 0

    hollow_men_found = False

    while cards_drawn < num_cards:
        drawn_card = draw_deck.pop()
        discard_deck.append(drawn_card)

        print('Card Drawn:' + drawn_card)

        if drawn_card == 'hollow men':
            print('Found hollow man, not a city')
            hollow_men_found = True
        elif hollow_men_found == True:
            print('Found a city - adding a hollow man')
            hollow_men_added[drawn_card] += 1
            if hollow_men_added[drawn_card] > 3:
                population_lost[drawn_card] += 1
            hollow_men_found = False
            cards_drawn += 1
        else:
            print('Found a city - no hollow men')
            cubes_lost[drawn_card] += 1
            cards_drawn += 1

#print draw_deck
#print discard_deck
#print hollow_men_added
#print population_lost
#print cubes_lost

drawCards(initial_draw)

#print draw_deck
#print discard_deck
#print hollow_men_added
#print population_lost
#print cubes_lost

def endTurn():
    global player_drawn
    global discard_deck
    global draw_deck
    global epidemic_count

    card1 = player_deck.pop()
    card2 = player_deck.pop()

    ### TODO: Handle double epidemics in one turn and card off the bottom
    if (card1 != 'epidemic') and (card2 != 'epidemic'):
        drawCards(infection_rate[epidemic_count])
    else:
        print('EPIDEMIC DRAWN!')
        random.shuffle(discard_deck)
        draw_deck = draw_deck + discard_deck
        discard_deck = []
        drawCards(infection_rate[epidemic_count])
        epidemic_count += 1

        #print draw_deck
        #print discard_deck
        #print hollow_men_added
        #print population_lost
        #print cubes_lost

    player_drawn += 2

active_turn = 0

while active_turn < turns_to_simulate:
    endTurn()
    active_turn += 1


print(draw_deck)
print(discard_deck)
print(hollow_men_added)
print(population_lost)
print(cubes_lost)
print(player_deck)

total_pop_lost = sum(population_lost.values())
total_cubes_lost = sum(cubes_lost.values())
total_men_added = sum(hollow_men_added.values())
cities_blocked_list = [x for x in hollow_men_added.values() if x > 0]
cities_blocked = len(cities_blocked_list)

print('TOTAL POPULATION LOST: ' + str(total_pop_lost))
print('TOTAL CUBES LOST: ' + str(total_cubes_lost))
print('TOTAL HOLLOW MEN: ' + str(total_men_added))
print('CITIES BLOCKED: ' + str(cities_blocked))
