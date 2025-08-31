import random 
import time 
from move import Move 
from item import Item 
from utils import *

class Pokemon():
    def __init__(self, name, lvl, baseAtk, baseDef, baseSpd, moveset, hp, bolsa_espaco):     
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
        self.hp = hp
        self.status = None
        self.bolsa_espaco = bolsa_espaco
        self.vitoria = False
        self.captured = False
        self.turno= False
        self.last_used_move = None
        self.critical = 1.50

    def turno_contra_o_jogador(self, move, jogador):
        mostrar_hp(jogador, self)
        if self.calcular_chance_de_acerto(move):
            time.sleep(1.5)
            mostrar_hp(jogador, self)
            print(self.logica_do_ataque(move, jogador))
            time.sleep(2)
        else:
            time.sleep(2)
            pass
            

    def escolher_ataque(self):
        print("========================================")
        print(f"II (1) {self.moveset[0].name}   (2) {self.moveset[1].name}       II")
        print(f"II (3) {self.moveset[2].name}   (4) {self.moveset[3].name}\t     II")
        print("========================================")

        index = int(input("Escolha um movimento e pressione 'Enter' ")) - 1
        return self.moveset[index]


    ##Sistema para calcular a chance do seu pokemon não atacar por algum motivo. 
    #        
    def calcular_chance_de_acerto(self, move):
        chance = random.randint(0, 100) 

        ## caso voce esteja paralizado, tem 20% de chance de errar o move

        if self.status == "paralyzed" and chance < 20:
            print(f"{self.name} não se mexe, está paralizado!") 
            return False 
        
        # chance de voce errar um move seja status ou attack

        elif move.type == 'Attack' or move.type == "status": 
            chance = random.randint(0, self.baseAccuracy) 
            print(f"{self.name} usou {move.name}! ")
            time.sleep(1)

            if chance > self.accuracy: #
                print(f"{self.name} errou o ataque!")
                return False
            
            else:
                return True

        elif move.type == 'self_status':
            print(f"{self.name} usou {move.name}! ")
            self.last_used_move = move
            print(f"DEBUG {move.name} foi para o last_used_move do jogador!")
            return True
         
    #calcular o dano com base no seu status de ataque e a defesa do inimigo e a diferença de niveis
    def calcular_dano(self, move, alvo):
        lvlFactor = (self.lvl / (alvo.lvl + 5) )
        formulaAtkDef = (self.attack ) / (alvo.defense)
        formula = formulaAtkDef * move.value 

        #20% do dano ser critico
        rate = random.randint(0, 100)
        if rate <= 20:
            self.damage = (lvlFactor * formula * self.critical) 
            
        else:
            self.damage = (lvlFactor * formula) 
            

    ##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
    def logica_do_ataque(self, move, alvo):
        time.sleep(1.5)
        if (move.type == 'Attack'):
            self.calcular_dano(move, alvo)

        elif (move.effect == "paralyze"):
            if (alvo.status != None and alvo.status != "paralyzed"):
                return ("O golpe falhou...")

            elif (alvo.status == "paralyzed"):
                return (f"{alvo.name} já está paralisado!") 

            else:
                alvo.status = "paralyzed"
                alvo.speed += (alvo.speed * (-0.5))
                return (f"{alvo.name} ficou paralisado")

        elif (move.effect == "evasive"):
            if self.evasivess >= 70:
                return "Evasiva não aumenta mais!"
            
            else: 
                self.evasivess += move.value 
                time.sleep(1)   
                return (f"{self.name} aumentou um pouco sua evasiva!")
            
        #há um limite de quantas vezes um move do tipo status pode ser usado.
        
        else:
            if self.limitar_golpe_status(move, alvo):
                return "Status do oponente não abaixa mais"
            
    
        #CHANCE DO OPONENTE DESVIAR DO GOLPE
        rate = random.randint(0, 100)
        if rate <= alvo.evasivess: 
            #mostrar_hp(self, alvo)
            return (f"{alvo.name} desviou do ataque!")
        
        else:
            #mostrar_hp(self, alvo)
            return self.processar_final_do_turno(move, alvo)

    #mostrar o que aconteceu se o oponente perdeu hp, defesa, força do ataque... etc

    def processar_final_do_turno(self, move, alvo):
        if move.type == "Attack":
            alvo.hp -= self.damage

            if self.critical:
                print("Ataque crítico!")
                time.sleep(1)
                

            return (f"{alvo.name} perdeu {self.damage:.0f} de HP! ")
        
        elif move.effect == "status_def":
            alvo.defense -= self.status_dmg
            return (f"{alvo.name} perdeu um pouco da defesa!")
        
        elif move.effect == "status_accuracy":
            alvo.accuracy -= self.status_dmg
            return (f"{alvo.name} perdeu um pouco da precisão dos golpes!")
        
        elif move.effect == "status_atk":
            alvo.attack -= self.status_dmg
            return (f"{alvo.name} perdeu um pouco da força dos golpes!")
        
    #verifica se há limite dos status do oponente serem reduzidos

    def limitar_golpe_status(self, move, alvo):
        if move.effect == "status_def":
            if  alvo.defense <= 10:
                self.status_dmg = 0
                return True
            else:
                self.status_dmg = alvo.defense * move.value
                return False
            
        elif (move.effect == "status_accuracy"):
            if  alvo.accuracy <= 10:
                self.status_dmg = 0
                return True
            else:
                self.status_dmg = alvo.accuracy * move.value
                return False
        
        elif (move.effect == "status_atk"):
            if  alvo.attack <= 10:
                self.status_dmg = 0
                return True
            else:
                self.status_dmg = alvo.attack * move.value
                return False
        
                    
    def capturavel(self):
        if self.hp < 30:
            return True
        else:
            return False

    def bolsa(self):
        while True:
            print("===================================================")
            
            for index, item in enumerate(self.bolsa_espaco, start = 1):
                print(f"({index}) {self.bolsa_espaco[index - 1].name} x {self.bolsa_espaco[index - 1].amount}")
            
            print("(0) Voltar (ainda não implementado)")
            print("===================================================")
        
            try:
                index = int(input("Escolha um item e pressione 'Enter' ")) - 1
                item = self.bolsa_espaco[index]
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
    
#função para o jogador atacar logo apos o oponente, quando estiver mais lento
def contra_atacar(jogador, move, alvo):    
    mostrar_hp(jogador, alvo)        
    if jogador.calcular_chance_de_acerto(move):
        print(jogador.logica_do_ataque(move, alvo))
        time.sleep(1.5)
        return True
    else:
        return True
            
            
        