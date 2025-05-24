import random, time, os

def WinnerChecker(player, target):
        if player.hp <= 0.1:
            print(f"{player.name} desmaiou!")
            return True
        elif target.hp <= 0.1:
            print(f"{target.name} desmaiou!")
            return True
        else:
            return False
    
def limpa_tela():
    return os.system('cls' if os.name == 'nt' else 'clear')#se for winodows limpa com o 'cls' senao o 'clear'

def show_hp(player, target):
    #função dá um limpa tela e mostra o hp
    os.system('cls' if os.name == 'nt' else 'clear')#se for winodows limpa com o 'cls' senao o 'clear'
    print("======================")
    print(f"II   {target.name} Lvl. {target.lvl} II")
    print(f"II   HP: {target.hp:<10.0f} II")   
    print("======================")  

    print("              ========================")
    print(f"              II  {player.name} Lvl. {player.lvl:<1} II")
    print(f"              II  HP: {player.hp:<14.0f}II")   
    print("              ========================") 


        


