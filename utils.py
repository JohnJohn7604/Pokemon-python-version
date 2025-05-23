import random, time


def WinnerChecker(player, target):
        if player.hp <= 0.1:
            print(f"{player.name} desmaiou!")
            return True
        elif target.hp <= 0.1:
            print(f"{target.name} desmaiou!")
            return True
        else:
            return False
    
    

        


