import time
import random

##FUNÇÕES DO JOGO

def showHP():
    print("======================")
    print(f"II   {opponent.name} Lvl. {opponent.lvl} II ")
    print(f"II   HP: {opponent.hp}        II ")   
    print("======================")  

    print("                ========================")
    print(f"                II  {player.name} Lvl. {player.lvl} II ")
    print(f"                II  HP: {player.hp}           II ")   
    print("                ========================")   


def showMoves():
    showHP()
    print("========================================")
    print(f"II (1) {player.moveset[0].name}    (2) {player.moveset[1].name}       II")
    print(f"II (3) {player.moveset[2].name}   (4) {player.moveset[3].name}         II")
    print("========================================")

    index = int(input("Escolha um movimento e pressione 'Enter' ")) - 1
    return player.moveset[index]
    
def menu():
    print("========================================")
    print(f"II (1) LUTAR        (2)    BOLSA      II")
    print(f"II                  (3)    FUGIR      II")
    print("========================================")

    return input("Escolha uma opção e pressione 'Enter' ")
    
def changeTurn():
    global opponent, player
    change = opponent
    opponent = player
    player = change

##CLASSES

class Pokemon:
    def __init__(self, name, baseAtk, baseDef, baseSpd, baseSpAtk, 
baseSpDef, moveset):
        self.name = name
        self.lvl = 5
        self.baseAtk = baseAtk
        self.baseDef = baseDef
        self.baseSpd = baseSpd
        self.baseSpAtk = baseSpAtk
        self.baseSpDef = baseSpDef
        self.acuracy = 8.0 #standard: 8  max: 8
        self.evasivess = 5.0 #standard to lvl 5: 5 max: 10 
        self.moveset = moveset
        self.hp = 100.0
        self.status = None

    ##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
    def attackLogic(self, move):
        global lastAttack
        if (move.type == 'spAttack' or move.type == 'Attack'):
            opponent.hp -= move.value 
            print(f"{opponent.name} perdeu {move.value} de HP! ")

        elif (move.effect == "acuracy"):
            newValue = opponent.acuracy * move.value
            opponent.acuracy -= newValue
            print(f"{opponent.name} perdeu um pouco da precisão dos golpes!")

        elif (move.effect == "paralyze"):
            if (opponent.status != None and opponent.status != "paralyzed"):
                print("O golpe falhou...")

            elif (opponent.status == "paralyzed"):
                print(f"{opponent.name} já está paralizado!") 

            else:
                opponent.status = "paralyzed"
                opponent.baseSpd += (opponent.baseSpd * (-0.5))
                print(f"{opponent.name} ficou paralizado")

        elif (move.effect == "evasive"):
            newValue = player.evasivess * move.value
            player.evasivess += newValue
            print(f"{player.name} aumentou um pouco sua evasiva!")

        elif (move.effect == "def"):
            newValue = opponent.baseDef * move.value
            opponent.baseDef -= newValue
            print(f"{opponent.name} perdeu um pouco da defesa!")

        elif (move.effect == "atk"):
            newValue = opponent.baseAtk * move.value
            opponent.baseAtk -= newValue
            print(f"{opponent.name} perdeu um pouco da força dos golpes!")

        time.sleep(2.5)

##Sistema para calcular a chance do status do seu pokemon faze-lo não atacar.
    def attackChance(self, move):
        chance = random.randint(0, 100) 
        if self.status == "paralyzed" and chance < 20:
            print(f"{self.name} não se mexe, está paralizado!") 
        else:
            print(f"{self.name} usou {move.name}! ")
            time.sleep(2.5)
                    
            self.attackLogic(move)

    #Sistema para identificar quem ataca primeiro
    def whoAttackFirst(self, speed, move):
        global yourTurn, lastAttack
        #debug
        #print(f"player speed: {speed}, opponent speed:{opponent.baseSpd}") 
        if speed > opponent.baseSpd:
            self.attackChance(move)
        else:
            print("Oponente atacou pq vc está mais lento")    
            changeTurn()
            yourTurn = False
            player.attack(thunderWave)

            changeTurn()
            yourTurn = True
            self.attackChance(move)
            lastAttack = player

    def attack(self, move):
        #debug
        #print(f"{self.name}")
        global yourTurn
        if yourTurn == True:
            self.whoAttackFirst(self.baseSpd, move)

        else:
        #debug 
            #print("o oponente vai te atacar pq é a vez dele no turno")    
            self.attackChance(move)
               
            time.sleep(2.5)
                    
            
  
    
        

#BANCO DE ATAQUES                
class Move:
    def __init__(self, name, type, acuracy, value, effect):
        self.name = name
        self.type = type
        self.acuracy = acuracy
        self.value = value
        self.effect = effect

ember = Move("Ember", "spAttack", 100, 35, None)  ##
smokeScreen = Move("Smokescreen", 'status', 100, 0.15, "acuracy")
tackle = Move("Tackle", "Attack", 100, 20, None) ##
tailWhip = Move("Tail Whip", "status", 90, 0.15, "def")
thunderBolt = Move("Thunderbolt", "spAttack", 100, 90, None)
doubleTeam = Move("Double Team", "self_status", 100, 0.15, "evasive")
growl = Move("Growl", "status", 100, 0.15, "atk")
thunderWave = Move("Thunderwave", "status", 100, 0, "paralyze")

################################

#POKEMONS

#Charmander
charmanderMove = [ember, smokeScreen, tackle, tailWhip]
charmander = Pokemon("Charmander", 52, 43, 95, 60, 50, charmanderMove)

#Pikachu
pikachuMove = [thunderBolt, thunderWave, doubleTeam, growl]
pikachu = Pokemon("Pikachu", 55, 40, 90, 60 , 50, pikachuMove)

#main
victory = False
opponent = pikachu
player = charmander
yourTurn = True
lastAttack = opponent

while (victory == False):
    #debug
    #print("inicio do laço")
    #print(f"player {player.name} opp:{opponent.name}\n")

    if yourTurn == False:
        changeTurn()
        player.attack(random.choice(pikachuMove))  #DEBUG
        #player.attack(random.choice(pikachuMove))
        changeTurn()
        yourTurn = True

    else:
        showHP()
        userInput = menu()

        if userInput == '1':
            player.attack(showMoves())
            if lastAttack == player:
                yourTurn == True
            else:
                yourTurn = False
            
            time.sleep(2)

        elif userInput == '2':
            print("Not implemented")
            time.sleep(2)
            pass

        else:
            print('Você fugiu da batalha')
            time.sleep(2)
            break
