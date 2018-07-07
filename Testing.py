
from GameClasses import *

f = open('InfectionDeck.txt')
InfectionDeckList = f.read().splitlines()
f.close()

PlayerDeckList = {}
f = open('Player Deck.txt')
for line in f.read().splitlines():
    # second element is the number of cards
    PlayerDeckList[line.split(',')[0]] = line.split(',')[1]

infection = InfectionDeck(InfectionDeckList)

player = PlayerDeck(PlayerDeckList)

g = PandemicGame('testing',1,InfectionDeckList,PlayerDeckList,8)
print(g.status_report())

for i in range(10):
    print(infection.draw_top())

print(infection.epidemic())

for i in range(12):
    print(infection.draw_top())

print(player.setup(8))

for i in range(20):
    print(player.draw_top())