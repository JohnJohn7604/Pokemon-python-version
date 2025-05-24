import time
from utils import show_hp

class Item:
    def __init__(self, name, hp, pokeball, status, value, amount):
        self.name = name
        self.hp = hp
        self.pokeball = pokeball
        self.status = status
        self.value = value
        self.amount = amount

    def itemLogic(self, player, target):
            if self.hp:
                oldHp = player.hp
                newHp = self.value + oldHp
                
                if oldHp == 100:
                    show_hp(player, target)
                    print("Não irá ter efeito")
                    time.sleep(1)
                    return True, False
                
                if newHp > 100:
                    hp_gain = 100 - oldHp
                    player.hp = 100
                else:
                    hp_gain = self.value 
                    player.hp += hp_gain    

                show_hp(player, target)
                print(f"{player.name} usou {self.name}!")
                time.sleep(1.5)
                print(f"{player.name} encheu {hp_gain:.0f} do seu HP")
                return False, False

            if self.status == "desparalyze":

                if player.status == "paralyzed":
                    player.status = None
                    player.speed = player.baseSpd
                    show_hp(player, target)
                    print(f"{player.name} usou {self.name}!")
                    show_hp(player, target)
                    print(f"{player.name} curou paralisia!")
                    return False, False
                else:
                    show_hp(player, target)
                    print("Não irá ter efeito")
                    time.sleep(1)
                    return True, False

            if self.pokeball:
                
                capturable = target.captureRate()
                show_hp(player, target)
                print(f"{player.name} usou a Pokebola!")
                if capturable:
                    time.sleep(1.7)
                    show_hp(player, target)
                    print(f"..")
                    time.sleep(1)
                    show_hp(player, target)
                    print(f"...")
                    time.sleep(1)
                    show_hp(player, target)
                    print(f"Parabéns você capturou um {target.name}!!")
                    return False,  True
                    
                
                else: 
                    time.sleep(1.7)
                    show_hp(player, target)
                    print(f"..")
                    time.sleep(1)
                    show_hp(player, target)
                    print(f"...")
                    time.sleep(1)
                    show_hp(player, target)
                    print("Ah não! pensei ter capturado!")
                    return False, False
                
    def itemCount(self, player):
        self.amount -= 1
        if self.amount == 0:# se o item acabar ele é removido da bolsa
            player.bagslot.remove(self)