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
        self.acuracy = 8.0 #standard: 8  max: 8
        self.evasivess = 5.0 #standard to lvl 5: 5 max: 10 
        self.moveset = moveset
        self.hp = 100.0
        self.status = "paralyzed"
        self.bagslot = bagslot

    def damageCalculator(self, move, atk, targetdef):
        lvlFactor = (self.lvl / (target.lvl + 5) )
        formulaAtkDef = (atk ) / (targetdef)
        formula = formulaAtkDef * move.value 
        return lvlFactor * formula  
        

    ##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
    def attackLogic(self, move):
        global lastAttack
        if (move.type == 'spAttack'):
            damage = self.damageCalculator(move, self.baseSpAtk, target.baseSpDef)
            target.hp -= damage
            print(f"{target.name} perdeu {damage} de HP! ")

        elif (move.type == 'Attack'):
            damage = self.damageCalculator(move, self.baseSpAtk, target.baseSpDef)
            target.hp -= damage
            print(f"{target.name} perdeu {damage} de HP! ")

        elif (move.effect == "acuracy"):
            newValue = target.acuracy * move.value
            target.acuracy -= newValue
            print(f"{target.name} perdeu um pouco da precisão dos golpes!")

        elif (move.effect == "paralyze"):
            if (target.status != None and target.status != "paralyzed"):
                print("O golpe falhou...")

            elif (target.status == "paralyzed"):
                print(f"{target.name} já está paralizado!") 

            else:
                target.status = "paralyzed"
                target.baseSpd += (target.baseSpd * (-0.5))
                print(f"{target.name} ficou paralizado")

        elif (move.effect == "evasive"):
            newValue = player.evasivess * move.value
            player.evasivess += newValue
            print(f"{player.name} aumentou um pouco sua evasiva!")

        elif (move.effect == "def"):
            newValue = target.baseDef * move.value
            target.baseDef -= newValue
            print(f"{target.name} perdeu um pouco da defesa!")

        elif (move.effect == "atk"):
            newValue = target.baseAtk * move.value
            target.baseAtk -= newValue
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
    def whoAttackFirst(self, speed, move):
        global yourTurn, lastAttack
        #debug
        #print(f"player speed: {speed}, target speed:{target.baseSpd}") 
        if speed > target.baseSpd:
            self.attackChance(move)
        else:
            print("Oponente atacou primeiro vc está mais lento")    
            changeTurn()
            yourTurn = False
            #player.attack(random.choice(target.moveset))
            #debug
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

    def itemLogic(self, item):
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
                print(f"{player.name} curou paralisia!")
            else:
                print("Não teve efeito")

    def bag(self, item):
        print(f"{player.name} usou {item.name}!")
        return self.itemLogic(item)
    


#BANCO DE ATAQUES                
class Move:
    def __init__(self, name, type, acuracy, value, effect):
        self.name = name
        self.type = type
        self.acuracy = acuracy
        self.value = value
        self.effect = effect

ember = Move("Ember", "spAttack", 100, 35.0, None)  ##
smokeScreen = Move("Smokescreen", 'status', 100, 0.15, "acuracy")
tackle = Move("Tackle", "Attack", 100, 20.0, None) ##
tailWhip = Move("Tail Whip", "status", 90, 0.15, "def")
thundershock = Move("ThunderShock", "spAttack", 100, 40.0, None)
doubleTeam = Move("Double Team", "self_status", 100, 0.15, "evasive")
growl = Move("Growl", "status", 100, 0.15, "atk")
thunderWave = Move("Thunderwave", "status", 100, 0, "paralyze")

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
pokeball = Item("Pokebola", False, "", False, 30.0)


charmanderBag = [potion, desparalyze, pokeball]
pikachuBag = [potion, desparalyze, pokeball]
#POKEMONS

#Charmander
charmanderMove = [ember, smokeScreen, tackle, tailWhip]
charmander = Pokemon("Charmander", 5, 52, 43, 95, 60, 50, charmanderMove, charmanderBag)

#Pikachu
pikachuMove = [thundershock, thunderWave, doubleTeam, growl]
pikachu = Pokemon("Pikachu", 5, 55, 40, 90, 50, 50, pikachuMove, pikachuBag)


#main
victory = False
target = pikachu
player = charmander
yourTurn = True
lastAttack = target

while (victory == False):
    #debug
    #print("inicio do laço")
    #print(f"player {player.name} opp:{target.name}\n")

    if yourTurn == False:
        changeTurn()
        player.attack(thunderWave)  #DEBUG
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
            showHP()
            print(player.bag(showBag()))
            yourTurn = False
            time.sleep(2)
            pass

        else:
            print('Você fugiu da batalha')
            time.sleep(2)
            break
