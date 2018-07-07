"""
File to run different models of the game

Currently just a template file - the game class hasn't been written yet
"""
from GameClasses import *

"""
General Settings
"""
games_to_run = 1000
#To report all turns - good for debugging
#turns_to_report = range(100)
#To report every 5 turns - better to reduce file size
turns_to_report = range(5, 100, 5)

list_of_cities = ['new york','washington','london','chicago','denver',
    'san francisco','atlanta','paris','st petersburg','johannesburg',
    'sao paolo','jacksonville','lagos','mexico city','los angeles',
    'buenos aires','bogota','santiago','lima','dar es salaam','istanbul',
    'tripoli','antanarivo','moscow','baghdad']

report_by_turn_keys = ['total_cubes_removed', 'total_cubes_removed_above_pop', 'total_hollow_men_dropped',
                       'total_hollow_men_pop_loss', 'unique_cities_with_hollow_men', 'special_player_cards_drawn'
                       'searchable_player_cards_drawn', 'epidemics_drawn']

report_by_game_keys = ['time to 8 cubes above pop', '1st epidemic turn', '2nd epidemic turn',
                       '3rd epidemic turn', '4th epidemic turn', '5th epidemic turn', '6th epidemic turn',
                       '7th epidemic turn', '8th epidemic turn', '9th epidemic turn', '10th epidemic turn',
                       ]

city_out_file = 'CityResults.csv'
turn_out_file = 'TurnResults.csv'
game_out_file = 'GameResults.csv'

#Open output files:
city_file = open(city_out_file, 'w')
turn_file = open(turn_out_file, 'w')
game_file = open(game_out_file, 'w')

#Print headers for the CSV files
city_header = 'Model Name,Run Number,Turn Number,Data,'
for city in list_of_cities:
    city_header += city + ','
city_header += 'Total'
city_header = city_header.lstrip(',')
city_header = city_header.strip(',')
city_header += '\n'
city_file.write(city_header)

turn_header = 'Model Name,Run Number,Turn Number,'
for key in report_by_turn_keys:
    turn_header += key + ','
turn_header = turn_header.lstrip(',')
turn_header = turn_header.strip(',')
turn_header += '\n'
turn_file.write(turn_header)

game_header = 'Model Name, Run Number,'
for key in report_by_game_keys:
    game_header += key + ','
game_header = game_header.strip(',')
game_header = game_header.lstrip(',')
game_header += '\n'
game_file.write(game_header)


# Game Procs
def execute_game(model_name, infection_deck_path, player_deck_path):
    '''
    Run a model of games

    :param model_name: Name of the model to run
    :param infection_deck: The path to the file that is the description for the infection deck
    :param player_deck: The path to the file that is the description for the player deck
    :return:
    '''
    for game_num in range(games_to_run):
        inf_file = open(infection_deck_path)
        infection_deck = inf_file.read().splitlines()
        inf_file.close()

        player_deck = {}
        player_file = open('Player Deck.txt')
        for line in player_file.read().splitlines():
            # second element is the number of cards
            player_deck[line.split(',')[0]] = line.split(',')[1]

        p = PandemicGame(model_name, game_num, infection_deck, player_deck)

        game_end_found = 0
        turn_number = 1

        while game_end_found == 0:
            try:
                p.end_turn()
            except GameOverError:
                game_end_found = 1

            if turn_number in turns_to_report:
                record_turn_results(model_name, game_num, turn_number, p.status_report())

            turn_number += 1

        record_game_results(model_name, game_num, p.status_report())


def record_turn_results(model_name, game_num, turn_number, status_dict):
    '''
    Print the results to a CSV file that are interesting by turn.

    Things to capture:
        Number of cubes removed by city
        Number of hollow men dropped by city
        Hollow men population loss by city
        Unique cities with hollow men
        Total cubes removed
        Total Hollow men lost
        Total cubes removed over population
        Number of epidemics happened
        Upgraded player deck cards drawn
        Searchable cards drawn

    :param model_name: The name of the game to record
    :param game_num: The specific game number
    :param turn_number: The turn number for the game
    :param status_dict: a dump of the current status from the game object
    :return:
    '''

    report_by_city_keys = ['cubes_removed_by_city', 'hollow_men_dropped_by_city', 'hollow_men_pop_loss_by_city']

    for key in report_by_city_keys:

        printstr = ''
        printstr += model_name + ','
        printstr += str(game_num) + ','
        printstr += str(turn_number) + ','
        printstr += key + ','

        report_sum = 0

        report = status_dict.get(key,{})
        for city in list_of_cities:
            entry = report.get(key,{}).get(city, 0)
            report_sum += entry
            printstr += str(entry) + ','

        printstr += str(report_sum)
        printstr = printstr.strip(',')
        printstr = printstr.lstrip(',')
        printstr += '\n'

        city_file.write(printstr)

    print_turnstr = ''
    print_turnstr += model_name + ','
    print_turnstr += str(game_num) + ','
    print_turnstr += str(turn_number) + ','

    for key in report_by_turn_keys:
        entry = status_dict.get(key,0)
        print_turnstr += str(entry) + ','

    print_turnstr = print_turnstr.strip(',')
    print_turnstr = print_turnstr.lstrip(',')
    print_turnstr += '\n'

    turn_file.write(print_turnstr)


def record_game_results(model_name, game_num, status_dict):
    '''
    Print the results to a CSV file that are interesting at the end of the game

    Things to capture:
        Time to 8 cubes above population
        Time to first epidemic
        Time to second epidemic
        Time to third epidemic
        Time to fourth epidemic
        Time to fifth epidemic
        Time to sixth epidemic
        Time to seventh epidemic
        Time to eighth epidemic
        Time to ninth epidemic
        Time to tenth epidemic

    :param model_name: The name of the game to record
    :param game_num: The specific game number
    :param status_dict: a dump of the current status from the game object
    :return:
    '''

    print_gamestr = ''
    print_gamestr += model_name + ','
    print_gamestr += str(game_num) + ','
    print_gamestr += str(status_dict.get('turns_to_8_cubes_above_pop','N/A')) + ','

    epidemic_dict = status_dict.get('epidemic_timing', {})
    for epidemic_num in range(10):
        print_gamestr += str(epidemic_dict.get(epidemic_num, 'N/A')) + ','

    print_gamestr = print_gamestr.strip(',')
    print_gamestr = print_gamestr.lstrip(',')
    print_gamestr += '\n'

    game_file.write(print_gamestr)


"""
Execute Games
Baseline game should be our exact game settings at this point and represent Late June game
"""
model_name_1 = 'Baseline'
infection_deck_1 = 'InfectionDeck.txt'
player_deck_1 = 'Player Deck.txt'
execute_game(model_name_1, infection_deck_1, player_deck_1)
print('Finished Game #1')

model_name_2 = 'Baseline - no hollow men'
infection_deck_2 = 'InfectionDeckNoHollowMen.txt'
player_deck_2 = 'Player Deck.txt'
execute_game(model_name_2, infection_deck_2, player_deck_2)
print('Finished Game #2')

model_name_3 = 'No Three Card Cities'
infection_deck_3 = 'InfectionDeckNoThrees.txt'
player_deck_3 = 'Player Deck.txt'
execute_game(model_name_3, infection_deck_3, player_deck_3)
print('Finished Game #3')

model_name_4 = 'No One Card Cities'
infection_deck_4 = 'InfectionDeckNoOnes.txt'
player_deck_4 = 'Player Deck.txt'
execute_game(model_name_4, infection_deck_4, player_deck_4)
print('Finished Game #4')

model_name_5 = '36 City Cards'
infection_deck_5 = 'InfectionDeck.txt'
player_deck_5 = 'Player Deck36Cards.txt'
execute_game(model_name_5, infection_deck_5, player_deck_5)
print('Finished Game #5')

model_name_6 = '37 City Cards'
infection_deck_6 = 'InfectionDeck.txt'
player_deck_6 = 'Player Deck37Cards.txt'
execute_game(model_name_6, infection_deck_6, player_deck_6)
print('Finished Game #6')

model_name_7 = '44 City Cards'
infection_deck_7 = 'InfectionDeck.txt'
player_deck_7 = 'Player Deck44Cards.txt'
execute_game(model_name_7, infection_deck_7, player_deck_7)
print('Finished Game #7')

model_name_8 = '45 City Cards'
infection_deck_8 = 'InfectionDeck.txt'
player_deck_8 = 'Player Deck45Cards.txt'
execute_game(model_name_8, infection_deck_8, player_deck_8)
print('Finished Game #8')

model_name_9 = '52 City Cards'
infection_deck_9 = 'InfectionDeck.txt'
player_deck_9 = 'Player Deck52Cards.txt'
execute_game(model_name_9, infection_deck_9, player_deck_9)
print('Finished Game #9')

model_name_10 = '53 City Cards'
infection_deck_10 = 'InfectionDeck.txt'
player_deck_10 = 'Player Deck53Cards.txt'
execute_game(model_name_10, infection_deck_10, player_deck_10)
print('Finished Game #10')

#Close Output Files
city_file.close()
turn_file.close()
game_file.close()