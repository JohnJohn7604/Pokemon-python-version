def changeTurn(player, target):
    return target, player

def showHP(player, target):
    print("======================")
    print(f"II   {target.name} Lvl. {target.lvl} II ")
    print(f"II   HP: {target.hp:.0f}        II ")   
    print("======================")  

    print("                ========================")
    print(f"                II  {player.name} Lvl. {player.lvl} II ")
    print(f"                II  HP: {player.hp:.0f}             II ")   
    print("                ========================")   

def showMoves(player):
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

##colocar target e player como atributos    


