"""
File to run different models of the game

Currently just a template file - the game class hasn't been written yet
"""

"""
General Settings
"""
games_to_run = 100


"""
Game specific settings
Baseline game should be our exact game settings at this point and represent Late June game
"""
model_name_1 = 'Baseline'
infection_deck_1 = []
player_deck_1 = []

# Execute Game
for game_num in range(games_to_run):
    #p = PandemicGame(model_name_1, game_num, infection_deck_1, player_deck_1)
    #p.execute_game(100)

"""
Game specific settings
Game should be the same city cards as baseline, just no hollow men cards to see how much hollow men have changed the game
"""
model_name_2 = 'Baseline - no hollow men'
infection_deck_2 = []
player_deck_2 = []

# Execute Game
for game_num in range(games_to_run):
    #p = PandemicGame(model_name_2, game_num, infection_deck_2, player_deck_2)
    #p.execute_game(100)