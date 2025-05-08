import time
import random

##FUNÇÕES DO JOGO

def showHP():
    print("======================")
    print(f"II   {target.name} Lvl. {target.lvl} II ")
    print(f"II   HP: {target.hp:.0f}        II ")   
    print("======================")  

    print("                ========================")
    print(f"                II  {player.name} Lvl. {player.lvl} II ")
    print(f"                II  HP: {player.hp:.0f}           II ")   
    print("                ========================")   

####
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
    global target, player
    change = target
    target = player
    player = change

def showBag():
    print("===================================================")
    print(f"II (1) {player.bagslot[0].name} (2) {player.bagslot[1].name} II")
    print(f"II                         (3) {player.bagslot[2].name} II")
    print("===================================================")

    index = int(input("Escolha um item e pressione 'Enter' ")) - 1
    print(player.bagslot[index].name)
    return player.bagslot[index]


##CLASSES

class Pokemon:
    def __init__(self, name, lvl, baseAtk, baseDef, baseSpd, baseSpAtk, 
baseSpDef, moveset, bagslot):
        self.name = name
        self.lvl = lvl
        self.baseAtk = baseAtk
        self.baseDef = baseDef
        self.baseSpd = baseSpd
        self.baseSpAtk = baseSpAtk
        self.baseSpDef = baseSpDef
        self.baseAccuracy = 8.0 #standard: 8  max: 8
        self.baseEvasivess = 5.0 #standard to lvl 5: 5 max: 10 
        self.attack = None
        self.defense = None
        self.speed = None
        self.specialAtk = None
        self.specialDef = None
        self.accuracy = 8.0 #standard: 8  max: 8
        self.evasivess = 5.0 #standard to lvl 5: 5 max: 10 
        self.moveset = moveset
        self.hp = 100.0
        self.status = None
        self.bagslot = bagslot
        self.updateStats()
        

    def updateStats(self):
        self.attack = self.baseAtk
        self.defense = self.baseDef
        self.speed = self.baseSpd
        self.specialAtk = self.baseSpAtk
        self.specialDef = self.baseSpDef 
        self.accuracy = self.baseAccuracy
        self.evasivess = self.baseEvasivess

    def damageCalculator(self, move, atk, targetdef):
        lvlFactor = (self.lvl / (target.lvl + 5) )
        formulaAtkDef = (atk ) / (targetdef)
        formula = formulaAtkDef * move.value 
        return lvlFactor * formula  
        

    ##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
    def attackLogic(self, move):
        global lastAttack
        if (move.type == 'spAttack'):
            damage = self.damageCalculator(move, self.specialAtk, target.specialDef)
            target.hp -= damage
            print(f"{target.name} perdeu {damage} de HP! ")

        elif (move.type == 'Attack'):
            damage = self.damageCalculator(move, self.attack, target.defense)
            target.hp -= damage
            print(f"{target.name} perdeu {damage} de HP! ")

        elif (move.effect == "accuracy"):
            newValue = target.accuracy * move.value
            target.accuracy -= newValue
            print(f"{target.name} perdeu um pouco da precisão dos golpes!")

        elif (move.effect == "paralyze"):
            if (target.status != None and target.status != "paralyzed"):
                print("O golpe falhou...")

            elif (target.status == "paralyzed"):
                print(f"{target.name} já está paralizado!") 

            else:
                target.status = "paralyzed"
                target.speed += (target.speed * (-0.5))
                print(f"{target.name} ficou paralizado")

        elif (move.effect == "evasive"):
            newValue = player.evasivess * move.value
            player.evasivess += newValue
            print(f"{player.name} aumentou um pouco sua evasiva!")

        elif (move.effect == "def"):
            newValue = target.defense * move.value
            target.defense -= newValue
            print(f"{target.name} perdeu um pouco da defesa!")

        elif (move.effect == "atk"):
            newValue = target.attack * move.value
            target.attack -= newValue
            print(f"{target.name} perdeu um pouco da força dos golpes!")

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
    def whoAttackFirst(self, move):
        global yourTurn, lastAttack
        #debug
        #print(f"player speed: {speed}, target speed:{target.speed}") 
        if self.speed > target.speed:
            self.attackChance(move)
        else:
            print("Oponente atacou primeiro vc está mais lento")    
            changeTurn()
            yourTurn = False
            #player.fight(random.choice(target.moveset))
            #debug
            player.fight(thundershock)

            changeTurn()
            yourTurn = True
            self.attackChance(move)
            lastAttack = player

    def fight(self, move):
        #debug
        #print(f"{self.name}")
        global yourTurn
        if yourTurn == True:
            self.whoAttackFirst(move)

        else:
        #debug 
            #print("o oponente vai te atacar pq é a vez dele no turno")    
            self.attackChance(move)
               
            time.sleep(2.5)

    def itemLogic(self, item):
        global victory #debug
        if item.hp == True:
            oldHp = player.hp
            newHp = player.hp + item.value
            if oldHp == 100:
                message = "Não teve efeito"
                return message
            
            if newHp > 100:
                value = 100 - oldHp
                player.hp = 100
            else:
                pass

            message = f"{player.name} encheu {value} do seu HP"
            return message

        if item.status == "desparalyze":

            if self.status == "paralyzed":
                player.status = None
                player.speed = player.baseSpd
                print(f"{player.name} curou paralisia!")
                #debug = True
            else:
                print("Não teve efeito")

        if item.pokeball == True:
            
            capturable = target.captureRate()
            if capturable == True:
                print(f"..")
                time.sleep(1)
                print(f"...")
                time.sleep(1)
                print(f"Parabéns você capturou um {target.name}!!")
                time.sleep(2)
                victory = True

            else: 
                print(f"..")
                time.sleep(1)
                print(f"...")
                time.sleep(1)
                print("Ah não! pensei ter capturado!")

    def captureRate(self):
        if target.hp < 30:
            return True
        else:
            return False


    def bag(self, item):
        print(f"{player.name} usou {item.name}!")
        return self.itemLogic(item)
    


#BANCO DE ATAQUES                
class Move:
    def __init__(self, name, type, accuracy, value, effect):
        self.name = name
        self.type = type
        self.accuracy = accuracy
        self.value = value
        self.effect = effect

ember = Move("Ember", "spAttack", 100, 35.0, None)  ##
smokeScreen = Move("Smokescreen", 'status', 100, 0.15, "accuracy")
tackle = Move("Tackle", "Attack", 100, 20.0, None) ##
tailWhip = Move("Tail Whip", "status", 90, 0.15, "def")
thundershock = Move("ThunderShock", "spAttack", 100, 40.0, None)
doubleTeam = Move("Double Team", "self_status", 100, 0.15, "evasive")
growl = Move("Growl", "status", 100, 0.15, "atk")
thunderwave = Move("Thunderwave", "status", 100, 0, "paralyze")

################################

###ITEMS
class Item:
    def __init__(self, name, hp, pokeball, status, value):
        self.name = name
        self.hp = hp
        self.pokeball = pokeball
        self.status = status
        self.value = value

potion = Item("Poção",True, False, "", 20.0)
desparalyze = Item("Desparalizador", False, False, "desparalyze", 0.0)
pokeball = Item("Pokebola", False, True, False, 30.0)


charmanderBag = [potion, desparalyze, pokeball]
pikachuBag = [potion, desparalyze, pokeball]
#POKEMONS

#Charmander
charmanderMove = [ember, smokeScreen, tackle, tailWhip]
charmander = Pokemon("Charmander", 5, 52, 43, 95, 60, 50, charmanderMove, 
                     charmanderBag)
charmander.updateStats()

#Pikachu
pikachuMove = [thundershock, thunderwave, doubleTeam, growl]
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
    #print("inicio do laço")
    #print(f"player {player.name} opp:{target.name}\n")

    if yourTurn == False:
        changeTurn()
        #if player.status == "paralyzed":
        #    player.bag(player.bagslot[1])
        #else:
        if target.status == "paralyzed" or debug == True:
            player.fight(thundershock)
        else:    
            player.fight(thunderwave)  #DEBUG
            

        changeTurn()
        yourTurn = True

    else:
        showHP()
        userInput = menu()

        if userInput == '1':
            player.fight(showMoves())
            if lastAttack == player:
                yourTurn == True
            else:
                yourTurn = False
            
            time.sleep(2)

        elif userInput == '2':
            showHP()
            print(player.bag(showBag()))
            yourTurn = False
            time.sleep(2)
            pass

        else:
            print('Você fugiu da batalha')
            time.sleep(2)
            break
