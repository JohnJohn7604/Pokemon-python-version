import time, random
from classes import Pokemon, Item, Move
from functions import changeTurn, showHP, showMoves, menu, battle

ember = Move("Ember", "Attack", 100, 35.0, None)  ##
smokeScreen = Move("Smokescreen", 'status', 100, 0.15, "status_accuracy")
tackle = Move("Tackle", "Attack", 100, 20.0, None) ##
tailWhip = Move("Tail Whip", "status", 90, 0.17, "status_def")
thundershock = Move("ThunderShock", "Attack", 100, 40.0, None)
doubleTeam = Move("Double Team", "self_status", 100, 12, "evasive")
growl = Move("Growl", "status", 100, 0.17, "status_atk")
thunderwave = Move("Thunderwave", "status", 100, 0, "paralyze")
quickattack = Move("Quick Attack", "Attack", 100, 40, None)

###ITEMS
potion = Item("Poção",True, False, "", 20.0, 2)
desparalyze = Item("Desparalizador", False, False, "desparalyze", 0.0, 1)
pokeball = Item("Pokebola", False, True, False, 30.0, 3)

charmanderBag = [potion, desparalyze, pokeball]
pikachuBag = [potion, desparalyze, pokeball]
#POKEMONS

#Charmander
charmanderMove = [ember, smokeScreen, growl, tailWhip]
charmander = Pokemon("Charmander", 5, 52, 43, 95, charmanderMove, charmanderBag)
charmander.updateStats()

#Pikachu
pikachuMove = [quickattack, thunderwave, doubleTeam, tackle]
pikachu = Pokemon("Pikachu", 5, 55, 40, 90, pikachuMove, pikachuBag)
pikachu.updateStats()

#INICIO DA BATALHA
target = pikachu
player = charmander
yourTurn = True
victory = False

while (victory == False):
    yourTurn, victory = battle(player, target, yourTurn, victory)

if player.hp > target.hp:
    print("Fim da batalha!!")

