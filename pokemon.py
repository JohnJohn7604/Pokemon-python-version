import random 
import time 
from move import Move 
from item import Item 
from utils import *

class Pokemon():
    def __init__(self, name, lvl, baseAtk, baseDef, baseSpd, moveset, bagslot):     
        self.name = name
        self.lvl = lvl
        self.baseAtk = baseAtk
        self.baseDef = baseDef
        self.baseSpd = baseSpd
        self.baseAccuracy = 15 #standard: 15
        self.baseEvasivess = 15 #standard: 15 max: 70
        self.attack = self.baseAtk
        self.defense = self.baseDef
        self.speed = self.baseSpd
        self.accuracy = self.baseAccuracy
        self.evasivess = self.baseEvasivess
        self.moveset = moveset
        self.hp = 100
        self.status = None
        self.bagslot = bagslot
        self.last_move = None
        self.victory = False
        self.turn = False
        self.last_used_move = None

    def fight_with_player(self, move, player):
        if self.move_hit(move):
            print(self.attack_logic(move, player))
            time.sleep(2)
        else:
            time.sleep(2)
            pass
            

    def move_select(self):
        print("========================================")
        print(f"II (1) {self.moveset[0].name}    (2) {self.moveset[1].name}       II")
        print(f"II (3) {self.moveset[2].name}   (4) {self.moveset[3].name}         II")
        print("========================================")

        index = int(input("Escolha um movimento e pressione 'Enter' ")) - 1
        return self.moveset[index]


    ##Sistema para calcular a chance do seu pokemon não atacar por algum motivo.        
    def move_hit(self, move):
        chance = random.randint(0, 100) 
        ## caso voce esteja paralizado, tem 20% de chance de errar o move
        if self.status == "paralyzed" and chance < 20:
            print(f"{self.name} não se mexe, está paralizado!") 
            return False 
        
        elif move.type == 'Attack' or move.type == "status": # chance de voce errar um move 
            chance = random.randint(0, self.baseAccuracy)
            print(f"{self.name} usou {move.name}! ")
            time.sleep(1)

            if chance > self.accuracy: 
                print(f"{self.name} errou o ataque!")
                return False
            
            else:
                return True

        elif move.type == 'self_status':
            print(f"{self.name} usou {move.name}! ")
            return True
        
    #Sistema para identificar quem ataca primeiro
    def who_is_more_fast(self, target):
        #se sua velocidade está maior do que a do oponente vc ataca primeiro
        if self.speed > target.speed:
            return True
        else:
            print("Oponente irá atacar primeiro, pois você está mais lento\n")    
            time.sleep(1.5)
            return False 

    def critical_chance(self):
        rate = random.randint(0, 100)
        self.critical = 1.50
        return rate
         
    #calcular o dano com base no seu status de ataque e a defesa do inimigo e a diferença de niveis
    def damageCalculator(self, move, target):
        lvlFactor = (self.lvl / (target.lvl + 5) )
        formulaAtkDef = (self.attack ) / (target.defense)
        formula = formulaAtkDef * move.value 

        #20% do dano ser critico
        if self.critical_chance() <= 20:
            self.damage = (lvlFactor * formula * self.critical) 
            self.critical = True
        else:
            self.damage = (lvlFactor * formula) 
            self.critical = False

    ##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
    def attack_logic(self, move, target):
        time.sleep(1.5)
        if (move.type == 'Attack'):
            self.damageCalculator(move, target)

        elif (move.effect == "paralyze"):
            if (target.status != None and target.status != "paralyzed"):
                return ("O golpe falhou...")

            elif (target.status == "paralyzed"):
                return (f"{target.name} já está paralisado!") 

            else:
                target.status = "paralyzed"
                target.speed += (target.speed * (-0.5))
                return (f"{target.name} ficou paralisado")

        elif (move.effect == "evasive"):
            if self.evasivess >= 70:
                return "Evasiva não aumenta mais!"
            
            else: 
                self.evasivess += move.value 
                time.sleep(1)   
                return (f"{self.name} aumentou um pouco sua evasiva!")
            
        #se player escolhe um move do tipo status, mas há um limite de quantas vezes pode ser usado. 
        else:
            if self.status_limit(move, target):
                return "Status do oponente não abaixa mais"
            
        ##todo golpe usado no oponente tem uma chance dele se esquivar
        #CHANCE DO OPONENTE DESVIAR DO GOLPE
        if self.evassives_target_chance() <= target.evasivess: 
            return (f"{target.name} desviou do ataque!")
        
        else:
            return self.conclusion(move, target)

    #chance do oponente escapar
    def evassives_target_chance(self):
        rate = random.randint(0, 100)
        return rate

    def conclusion(self, move, target):
        if move.type == "Attack":
            target.hp -= self.damage

            if self.critical:
                print("Ataque crítico!")
                time.sleep(2)

            return (f"{target.name} perdeu {self.damage:.0f} de HP! ")
        
        elif move.effect == "status_def":
            target.defense -= self.status_dmg
            return (f"{target.name} perdeu um pouco da defesa!")
        
        elif move.effect == "status_accuracy":
            target.accuracy -= self.status_dmg
            return (f"{target.name} perdeu um pouco da precisão dos golpes!")
        
        elif move.effect == "status_atk":
            target.attack -= self.status_dmg
            return (f"{target.name} perdeu um pouco da força dos golpes!")
        
    #verifica se há limite dos status do oponente serem reduzidos
    def status_limit(self, move, target):
        if move.effect == "status_def":
            if  target.defense <= 10:
                self.status_dmg = 0
                return True
            else:
                self.status_dmg = target.defense * move.value
                return False
            
        elif (move.effect == "status_accuracy"):
            if  target.accuracy <= 10:
                self.status_dmg = 0
                return True
            else:
                self.status_dmg = target.accuracy * move.value
                return False
        
        elif (move.effect == "status_atk"):
            if  target.attack <= 10:
                self.status_dmg = 0
                return True
            else:
                self.status_dmg = target.attack * move.value
                return False
    
    def fight(self, move, target):
        last_player_move = move #move que sera usado, apos vc ser atacado por estar mais lento
        #sua vez
        if self.turn:
            you = self.who_is_more_fast(target)
            #se o seu pokemon for o mais rápido vc ira atacar primeiro
            if you:
                #verificação se o golpe será acertado
            
                if self.move_hit(move):
                    print(self.attack_logic(move, target))
                    time.sleep(1.5)
                    victory = WinnerChecker(self, target)
                    if victory:

                        return True
                    else:
                        return False
                
                else:
                    
                    return False
            
            else:
                #oponente ataca primeiro pois vc esta mais lento
                
                target_move = target.pikachu_ai(target.moveset[2])
                target.fight_with_player(target_move, self)
                target.last_used_move = target_move
                return (self.player_attacks(last_player_move, target))
                    
                
                
                    
       
        #vez do oponente apos ter recebido o seu golpe
        
            
            #se ele acertar, se vc ainda estiver vivo, ataca imediatamente
            


    def player_attacks(self, move, target):            
        if self.move_hit(move):
            print(self.attack_logic(move, target))
            time.sleep(1.5)
            return True
        else:
            return True
                    
        
                

    def captureRate(self):
        if self.hp < 30:
            return True
        else:
            return False

    def bag(self):
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

    def pikachu_ai(self, move):
        # move so sera retornado se for diferente de double team caso ele tenha sido o ultimo golpe.
        if self.last_used_move == self.moveset[2]: 
            while move == self.moveset[2]:
                move = random.choice(self.moveset)

        return move
            
        