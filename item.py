import time
from utils import mostrar_hp

class Item:
    def __init__(self, name, hp, pokeball, status, value, amount):
        self.name = name
        self.hp = hp
        self.pokeball = pokeball
        self.status = status
        self.value = value
        self.amount = amount

    def logica_desse_item(self, jogador, alvo):
            if self.hp:
                oldHp = jogador.hp
                newHp = self.value + oldHp
                
                if oldHp == 100:
                    mostrar_hp(jogador, alvo)
                    print("Não irá ter efeito")
                    time.sleep(1)
                    return True, False
                
                if newHp > 100:
                    hp_gain = 100 - oldHp
                    jogador.hp = 100
                else:
                    hp_gain = self.value 
                    jogador.hp += hp_gain    

                mostrar_hp(jogador, alvo)
                print(f"{jogador.name} usou {self.name}!")
                time.sleep(1.5)
                print(f"{jogador.name} encheu {hp_gain:.0f} do seu HP")
                return False, False

            if self.status == "desparalyze":

                if jogador.status == "paralyzed":
                    jogador.status = None
                    jogador.speed = jogador.baseSpd
                    mostrar_hp(jogador, alvo)
                    print(f"{jogador.name} usou {self.name}!")
                    mostrar_hp(jogador, alvo)
                    print(f"{jogador.name} curou paralisia!")
                    return False, False
                else:
                    mostrar_hp(jogador, alvo)
                    print("Não irá ter efeito")
                    time.sleep(1)
                    return True, False

            if self.pokeball:
                
                mostrar_hp(jogador, alvo)
                print(f"{jogador.name} usou a Pokebola!")
                if alvo.capturavel():
                    time.sleep(1.7)
                    mostrar_hp(jogador, alvo)
                    print(f"..")
                    time.sleep(1)
                    mostrar_hp(jogador, alvo)
                    print(f"...")
                    time.sleep(1)
                    mostrar_hp(jogador, alvo)
                    print(f"Parabéns você capturou um {alvo.name}!!")
                    return False,  True
                    
                
                else: 
                    time.sleep(1.7)
                    mostrar_hp(jogador, alvo)
                    print(f"..")
                    time.sleep(1)
                    mostrar_hp(jogador, alvo)
                    print(f"...")
                    time.sleep(1)
                    mostrar_hp(jogador, alvo)
                    print("Ah não! pensei ter capturado!")
                    return False, False
                
    def itemCount(self, jogador):
        self.amount -= 1
        if self.amount == 0:# se o item acabar ele é removido da bolsa
            jogador.bagslot.remove(self)