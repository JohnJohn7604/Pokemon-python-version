import random
import time

def changeTurn():
    global target, player
    change = target
    target = player
    player = change

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
        self.baseEvasivess = 80 #standard to lvl 5: 5 max: 10 
        self.attack = None
        self.defense = None
        self.speed = None
        self.specialAtk = None
        self.specialDef = None
        self.accuracy = 8.0 #standard: 8  max: 8
        self.evasivess = 50 #standard: 50 max: 10
        self.moveset = moveset
        self.hp = 100.0
        self.status = "paralyzed"
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

    def _criticalChance(self):
        rate = random.randint(0, 100)
        if rate <= 20:
            return 1.50
        else: 
            return 1.0

    def damageCalculator(self, move, atk, targetdef, target):
        lvlFactor = (self.lvl / (target.lvl + 5) )
        formulaAtkDef = (atk ) / (targetdef)
        formula = formulaAtkDef * move.value 

        critical = self._criticalChance()
        if critical > 1:
            return (lvlFactor * formula * critical), "Ataque crítico"
        else:
            return (lvlFactor * formula * critical), None

   #CHANCE DO OPONENTE DESVIAR DO GOLPE       
    def evassivesTargetChance(self, target):
        chance = random.randint(0, 100)
        if chance <= target.evasivess:
            return (True), (f"{target.name} desviou do ataque!")
        else:
            return (False), (None)
        
    ##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
    def attackLogic(self, move, yourTurn, target):
        if (move.type == 'spAttack'):
            damage, message = self.damageCalculator(move, self.specialAtk, target.specialDef, target)

        elif (move.type == 'Attack'):
            damage, message = self.damageCalculator(move, self.attack, target.defense, target)

        elif (move.effect == "accuracy"):
            newValue = target.accuracy * move.value
            target.accuracy -= newValue
            return False, (f"{target.name} perdeu um pouco da precisão dos golpes!")

        elif (move.effect == "paralyze"):
            if (target.status != None and target.status != "paralyzed"):
                return False, ("O golpe falhou...")

            elif (target.status == "paralyzed"):
                return False, (f"{target.name} já está paralizado!") 

            else:
                target.status = "paralyzed"
                target.speed += (target.speed * (-0.5))
                return False, (f"{target.name} ficou paralizado")

        elif (move.effect == "evasive"):
            self.evasivess += move.value 
            if self.evasivess > 80:
                return True, "Evasiva não aumenta mais!"
            else: 
                print(f"{self.name} usou {move.name}! ")
                time.sleep(1)   
                return False, (f"{self.name} aumentou um pouco sua evasiva!")

        elif (move.effect == "def"):
            newValue = target.defense * move.value
            target.defense -= newValue
            return False, (f"{target.name} perdeu um pouco da defesa!")

        elif (move.effect == "atk"):
            newValue = target.attack * move.value
            target.attack -= newValue
            return False, (f"{target.name} perdeu um pouco da força dos golpes!")

        targetEscape, message = self.evassivesTargetChance(target)
        if targetEscape:

            return False, message
        else:
            target.hp -= damage
            print(f"{target.name} perdeu {damage:.0f} de HP! ")
            time.sleep(1)

            return False, message
            
        time.sleep(2.5)

##Sistema para calcular a chance do seu pokemon não atacar por algum motivo.
    def attackChance(self, move, yourTurn, target):
        chance = random.randint(0, 100) 
        ## caso voce esteja paralizado
        if self.status == "paralyzed" and chance < 20:
            return False, (f"{self.name} não se mexe, está paralizado!") 
        # caso seu move seja um ataque ou altere algum atributo do oponente
        elif move.type == 'Attack' or move.type == "status":
            ## caso sua precisao esteja abaixo do normal
            chance = random.randint(0, self.baseAccuracy)
            print(f"{self.name} usou {move.name}! ")
            time.sleep(1)

            if chance > self.accuracy:
                return False, (f"{self.name} errou o ataque!")
           
        return (self.attackLogic(move, yourTurn, target))

    #Sistema para identificar quem ataca primeiro
    def whoAttackFirst(self, move, yourTurn, target):
        global lastAttack
        #debug
        #print(f"player speed: {speed}, target speed:{target.speed}") 
        if self.speed > target.speed:
            print(self.attackChance(move, yourTurn, target))
        else:
            print("Oponente atacou primeiro vc está mais lento")    
            changeTurn()
            yourTurn = False
            #self.fight(random.choice(target.moveset))
            #debug
            self.fight(thundershock)

            changeTurn()
            yourTurn = True
            print(self.attackChance(move))
            lastAttack = self

    def fight(self, move, yourTurn, target):
        #debug
        #print(f"{self.name}")
        if yourTurn:
            self.whoAttackFirst(move, yourTurn, target)

        else:
        #debug 
            #print("o oponente vai te atacar pq é a vez dele no turno")    
            tryAgain, message = (self.attackChance(move, yourTurn, target))
            if tryAgain:
                return self.fight(random.choice(self.moveset), yourTurn, target)

            else:
                print(message)
                yourTurn = True
               
            time.sleep(2.5)

        return yourTurn

    def itemLogic(self, item, target, victory):
        if item.hp:
            oldHp = self.hp
            
            if oldHp == 100:
                return True, "Não irá ter efeito"
            
            if newHp > 100:
                value = 100 - oldHp
                self.hp = 100
            else:
                newHp = self.hp + item.value
                print(f"{self.name} usou {item.name}!")

            return False, (f"{self.name} encheu {value} do seu HP")

        if item.status == "desparalyze":

            if self.status == "paralyzed":
                self.status = None
                self.speed = self.baseSpd
                print(f"{self.name} usou {item.name}!")
                
                return False, f"{self.name} curou paralisia!"
                #debug = True
            else:
                return True, "Não irá ter efeito"

        if item.pokeball:
            
            capturable = target.captureRate()
            if capturable:
                print(f"{self.name} usou a Pokebola!")
                time.sleep(1)
                print(f"..")
                time.sleep(1)
                print(f"...")
                time.sleep(1)
                victory = True
                return False, (f"Parabéns você capturou um {target.name}!!")
                time.sleep(2)
            
            else: 
                print(f"{self.name} usou a Pokebola!")
                time.sleep(1)
                print(f"..")
                time.sleep(1)
                print(f"...")
                time.sleep(1)
                return False, ("Ah não! pensei ter capturado!")

        item.amount -= 1
        if item.amount == 0:
            self.bagslot.remove(item)
        return ""

    def captureRate(self):
        if self.hp < 30:
            return True
        else:
            return False


    def bag(self, target, victory):
        print("===================================================")
        
        for index, item in enumerate(self.bagslot, start = 1):
            print(f"({index}) {self.bagslot[index - 1].name} x {self.bagslot[index - 1].amount}")
        
        print("===================================================")

        index = int(input("Escolha um item e pressione 'Enter' ")) - 1
        item = self.bagslot[index]
        return self.itemLogic(item, target, victory)
    
    #
    
#BANCO DE ATAQUES                
class Move:
    def __init__(self, name, type, accuracy, value, effect):
        self.name = name
        self.type = type
        self.accuracy = accuracy
        self.value = value
        self.effect = effect


class Item:
    def __init__(self, name, hp, pokeball, status, value, amount):
        self.name = name
        self.hp = hp
        self.pokeball = pokeball
        self.status = status
        self.value = value
        self.amount = amount