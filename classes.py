import random
import time
from functions import changeTurn, whoIsMoreFast, moveHitChance, attackLogic

class Pokemon:
    def __init__(self, name, lvl, baseAtk, baseDef, baseSpd, moveset, bagslot):
        self.name = name
        self.lvl = lvl
        self.baseAtk = baseAtk
        self.baseDef = baseDef
        self.baseSpd = baseSpd
        self.baseAccuracy = 11 #standard: 8  max: 8
        self.baseEvasivess = 10 #standard: 10 max: 70
        self.attack = None
        self.defense = None
        self.speed = None
        self.accuracy = None
        self.evasivess = None
        self.moveset = moveset
        self.hp = 100.0
        self.status = None
        self.bagslot = bagslot
        self.updateStats()
        

    def updateStats(self):
        self.attack = self.baseAtk
        self.defense = self.baseDef
        self.speed = self.baseSpd
        self.accuracy = self.baseAccuracy
        self.evasivess = self.baseEvasivess

    def _criticalChance(self):
        rate = random.randint(0, 100)
        #20% do dano ser critico
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
            return (lvlFactor * formula * critical), True
        else:
            return (lvlFactor * formula * critical), True

   #CHANCE DO OPONENTE DESVIAR DO GOLPE       
    def evassivesTargetChance(self, target):
        chance = random.randint(0, 100)
        #quanto maior o evasivess maior a chance de escapar
        if chance <= target.evasivess:
            return (True), (f"{target.name} desviou do ataque!")
        else:
            return (False), (None)
    
    def fight(self, move, target, yourTurn):
        print(f"{self.name}, {target.name}")
        player_move = move
        if yourTurn:
            you = whoIsMoreFast(self.speed, target.speed)

            if you:
                hit, message = moveHitChance(self, move, target)

                if hit:
                    print(attackLogic(self, move, target))
                    return False
                
                else:
                    print (message)
                    return False
            
            else:
                #target, player = changeTurn(self, target)
                #print(f"DEPOIS: {self.name}, {target.name}")
                target_move = target.moveset[2]
                hit, message = moveHitChance(target, target_move, self)

                if hit:
                    print(attackLogic(target, target_move, self))
                    time.sleep(2)

                    hit, message = moveHitChance(self, player_move, target)

                    if hit:
                        print(attackLogic(self, move, target))
                        return True
                
                    else:
                        print (message)
                        return True
            
        else:
            hit, message = moveHitChance(self, player_move, target)

            if hit:
                print(attackLogic(self, player_move, target))
                return True
        
            else:
                print (message)
                return True
                

    def captureRate(self):
        if self.hp < 30:
            return True
        else:
            return False

    def bag(self, target, victory):
        while True:
            print("===================================================")
            
            for index, item in enumerate(self.bagslot, start = 1):
                print(f"({index}) {self.bagslot[index - 1].name} x {self.bagslot[index - 1].amount}")
            
            print("(0) Voltar")
            print("===================================================")
        
            try:
                index = int(input("Escolha um item e pressione 'Enter' ")) - 1
                item = self.bagslot[index]
                return item
            except ValueError:
                print("escolha uma opção válida")
            except IndexError:
                print("escolha uma opção válida")
             

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