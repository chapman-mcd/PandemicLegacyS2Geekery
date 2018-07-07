"""
File to run different models of the game

Currently just a template file - the game class hasn't been written yet
"""
from GameClasses import *

"""
General Settings
"""
games_to_run = 100
turns_to_report = range(100)

city_out_file = 'CityResults.csv'
game_out_file = 'GameResults.csv'
summary_file = 'SummaryResults.csv'

list_of_cities = ['new york','washington','london','chicago','denver',
    'san francisco','atlanta','paris','st petersburg','johannesburg',
    'sao paolo','jacksonville','lagos','mexico city','los angeles',
    'buenos aires','bogota','santiago','lima','dar es salaam','istanbul',
    'tripoli','antanarivo','moscow','baghdad']

"""
Game specific settings
Baseline game should be our exact game settings at this point and represent Late June game
"""
model_name_1 = 'Baseline'
infection_deck_1 = []
player_deck_1 = []
execute_game(model_name_1, infection_deck_1, player_deck_1)

model_name_2 = 'Baseline - no hollow men'
infection_deck_2 = []
player_deck_2 = []
execute_game(model_name_2, infection_deck_2, player_deck_2)


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
        infection_deck = f.read().splitlines()
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
                game_end_found = 0

            if turn_number in turns_to_report:
                record_turn_results(model_name, game_num, turn_number, p.get_status())

            turn_number += 1

        record_game_results(model_name1, game_num, p.get_status())


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

    report_by_city_keys = ['cubes_by_city', 'hollow_men_by_city', 'population_loss_by_city']


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

