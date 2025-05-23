from utils import *
from pokemon import Pokemon
from item import Item
from move import Move 

class Game:
    def __init__(self):
        ###ITEMS
        potion = Item("Poção",True, False, "", 20.0, 2)
        desparalyze = Item("Desparalizador", False, False, "desparalyze", 0.0, 1)
        pokeball = Item("Pokebola", False, True, False, 30.0, 3)

        ##MOVES
        ember = Move("Ember", "Attack", 100, 35.0, None)  
        smokeScreen = Move("Smokescreen", 'status', 100, 0.15, "status_accuracy")
        tackle = Move("Tackle", "Attack", 100, 20.0, None) 
        tailWhip = Move("Tail Whip", "status", 90, 0.17, "status_def")
        thundershock = Move("ThunderShock", "Attack", 100, 40.0, None)
        doubleTeam = Move("Double Team", "self_status", 100, 12, "evasive")
        growl = Move("Growl", "status", 100, 0.17, "status_atk")
        thunderwave = Move("Thunderwave", "status", 100, 0, "paralyze")
        quickattack = Move("Quick Attack", "Attack", 100, 40, None)

        #POKEMONS
        charmanderBag = [potion, desparalyze, pokeball]
        charmanderMove = [ember, smokeScreen, growl, tailWhip]
        charmander = Pokemon("Charmander", 5, 52, 43, 95, charmanderMove, charmanderBag)
        #charmander.updateStats()

        pikachuBag = [potion, desparalyze, pokeball]
        pikachuMove = [quickattack, thunderwave, doubleTeam, tackle]
        pikachu = Pokemon("Pikachu", 5, 55, 40, 90, pikachuMove, pikachuBag)
        #pikachu.updateStats()

        self.target = pikachu
        self.player = charmander
        self.victory = False

    def show_hp(self):
        print("======================")
        print(f"II   {self.target.name} Lvl. {self.target.lvl} II ")
        print(f"II   HP: {self.target.hp:.0f}        II ")   
        print("======================")  

        print("                ========================")
        print(f"           II  {self.player.name} Lvl. {self.player.lvl} II ")
        print(f"                II  HP: {self.player.hp:.0f}             II ")   
        print("                ========================") 

    def main_menu(self):
        print("========================================")
        print(f"II (1) LUTAR        (2)    BOLSA      II")
        print(f"II                  (3)    FUGIR      II")
        print("========================================")

        return input("Escolha uma opção e pressione 'Enter' ")
    
    def WinnerChecker(self, player, target):
        if player.hp <= 0.1:
            print(f"{player.name} desmaiou!")
            return True
        elif target.hp <= 0.1:
            print(f"{target.name} desmaiou!")
            return True
        elif self.target_captured:
            return True
        else:
            return False


    def battle(self):
        player = self.player
        target = self.target
        player.turn = True
        target_captured = False

        while self.victory == False:
            
            if player.turn:
                self.victory = WinnerChecker(player, target)
                self.victory = target_captured

                if self.victory:
                    return ("Fim da batalha")
                
                self.show_hp()
                user_input = self.main_menu()

                if user_input == '1':
                    self.show_hp()
                    player_move = player.move_select()
                    player.turn = player.fight(player_move, target)
                    print("\n")
                    time.sleep(2)
                    
                elif user_input == '2':
                    try_again = True
                    self.show_hp()

                    while try_again:
                        player_item = player.bag()
                        try_again, target_captured = player_item.itemLogic(player, 
                        target)
            
                        if target_captured:
                            player.turn = True
                        else:
                            player_item.itemCount(player)
                            time.sleep(2)
                            player.turn = False
                    
                else:
                    print('Você fugiu da batalha')
                    time.sleep(2)
                    
            else:
                target_move = target.pikachu_ai(target.moveset[2])
                target.fight_with_player(target_move, player)  
                player.turn = True
        
                print("\n")