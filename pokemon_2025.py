import time
import random
from classes import Pokemon
from classes import Item
from classes import Move
from functions import changeTurn
from functions import showHP
from functions import showMoves
from functions import menu




##FUNÇÕES 


ember = Move("Ember", "Attack", 100, 35.0, None)  ##
smokeScreen = Move("Smokescreen", 'status', 100, 0.15, "accuracy")
tackle = Move("Tackle", "Attack", 100, 20.0, None) ##
tailWhip = Move("Tail Whip", "status", 90, 0.15, "def")
thundershock = Move("ThunderShock", "Attack", 100, 40.0, None)
doubleTeam = Move("Double Team", "self_status", 100, 10, "evasive")
growl = Move("Growl", "status", 100, 0.15, "atk")
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
charmander = Pokemon("Charmander", 5, 52, 43, 95, 60, 50, charmanderMove, 
                     charmanderBag)
charmander.updateStats()

#Pikachu
pikachuMove = [quickattack, thunderwave, doubleTeam, tackle]
pikachu = Pokemon("Pikachu", 5, 55, 40, 90, 50, 50, pikachuMove, pikachuBag)
pikachu.updateStats()


#main
victory = False
target = pikachu
player = charmander
yourTurn = True
lastAttack = target
debug = False

while (victory == False):
    #debug
    if yourTurn == False:
        player, target = changeTurn(player, target)
        print(f"{player.name},, {target.name}")
        #if player.status == "paralyzed":
        #    player.bag(player.bagslot[1])
        #else:
        if target.status == "paralyzed" or debug == True:
            yourTurn = player.fight(doubleTeam, yourTurn, target)
        else:    
            yourTurn = player.fight(doubleTeam, yourTurn, target)  #DEBUG
        
        yourTurn = True

    else:
        if player.name != "Charmander":
            player, target = changeTurn(player, target)
        
        showHP(player, target)
        userInput = menu()

        if userInput == '1':
            showHP(player, target)
            yourTurn = player.fight(showMoves(player), yourTurn, target)
            if lastAttack == player:
                yourTurn == True
            else:
                yourTurn = False
            
            time.sleep(2)

        elif userInput == '2':
            tryAgain = True
            showHP(player, target)
            while tryAgain:
                tryAgain, message = player.bag(target, victory)
                print(message)
                time.sleep(2)
            
            print(f"{player.name},, {target.name}")
            yourTurn = False
            time.sleep(2)

        else:
            print('Você fugiu da batalha')
            time.sleep(2)
            break
