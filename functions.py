import random, time



def changeTurn(player, target):
    print(f"ANTES: {player.name}, {target.name}")
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

def battle(player, target, yourTurn, victory):
    ##fazer logica da vitoria aqui
    victory = False 
    
    if yourTurn:
        showHP(player, target)
        userInput = menu()

        if userInput == '1':
            showHP(player, target)
            player_move = showMoves(player)
            yourTurn = player.fight(player_move, target, yourTurn)
            time.sleep(2)
            return yourTurn

        elif userInput == '2':
            tryAgain = True
            showHP(player, target)

            while tryAgain:
                player_item = player.bag(target, victory)
                tryAgain, message = itemLogic(player, player_item, target, victory)
                print(message)

            itemCount(player, player_item)
            time.sleep(2)
            yourTurn = False
            time.sleep(2)

        else:
            print('Você fugiu da batalha')
            time.sleep(2)
            
    else:
    
        yourTurn = target.fight(target.moveset[2], player, yourTurn)  
        return yourTurn
        
        

#Sistema para identificar quem ataca primeiro
def whoIsMoreFast(speed, target_speed):
    #se sua velocidade está maior do que a do oponente vc ataca primeiro
    if speed > target_speed:
        return True
    else:
        print("Oponente atacou primeiro vc está mais lento")    
        return False  
    
##Sistema para calcular a chance do seu pokemon não atacar por algum motivo.        
def moveHitChance(player, move, target):
    chance = random.randint(0, 100) 
    ## caso voce esteja paralizado, tem 20% de chance de errar o move
    if player.status == "paralyzed" and chance < 20:
        return (False), (f"{player.name} não se mexe, está paralizado!") 
    
    elif move.type == 'Attack' or move.type == "status": # chance de voce errar um move 
        chance = random.randint(0, player.baseAccuracy)
        print(f"{player.name} usou {move.name}! ")
        time.sleep(1)

        if chance > player.accuracy: 
            return (False), (f"{player.name} errou o ataque!")
        
        else:
            return (True), ("")

    else:
        print(f"{player.name} usou {move.name}! ")
        return (True), ("")

def statusCalculator(target, move):
    if move.effect == "status_def":
        if target.defense <= 10:
            return 0, True
        else:
            return target.defense * move.value, False
        
    elif (move.effect == "status_accuracy"):
        if target.accuracy <= 10:
            return 0, True
        else:
            return target.accuracy * move.value, False
       
    elif (move.effect == "status_atk"):
        if target.attack <= 10:
            return 0, True
        else:
            return target.attack * move.value, False
        
    
##CONDIÇÃO DO MOVE, CASO SEJA DE TIRAR DANO OU SE PROVOCA BUFFER AO OPP.
def attackLogic(player, move, target):
    if (move.type == 'Attack'):
        damage, critical = player.damageCalculator(move, player.attack, target.defense, target)

    elif (move.effect == "paralyze"):
        if (target.status != None and target.status != "paralyzed"):
            return ("O golpe falhou...")

        elif (target.status == "paralyzed"):
            return (f"{target.name} já está paralizado!") 

        else:
            target.status = "paralyzed"
            target.speed += (target.speed * (-0.5))
            return (f"{target.name} ficou paralizado")

    elif (move.effect == "evasive"):
        if player.evasivess >= 70:
            return "Evasiva não aumenta mais!"
        
        else: 
            player.evasivess += move.value 
            time.sleep(1)   
            return (f"{player.name} aumentou um pouco sua evasiva!")

    else:
        status_loss, status_limit = statusCalculator(target, move)
        if status_limit:
            return "Status do oponente não abaixa mais"

    ##todo golpe usado no oponente tem uma chance dele se esquivar
    targetEscape, message = player.evassivesTargetChance(target)

    if targetEscape:
        return message
    
    elif move.type == "Attack":
        target.hp -= damage
        if critical:
            print("Ataque crítico!")

        return (f"{target.name} perdeu {damage:.0f} de HP! ")
    
    elif move.effect == "status_def":
        target.defense -= status_loss
        return (f"{target.name} perdeu um pouco da defesa!")
    
    elif move.effect == "status_accuracy":
        target.accuracy -= status_loss
        return (f"{target.name} perdeu um pouco da precisão dos golpes!")
    
    elif move.effect == "status_atk":
        target.attack -= status_loss
        return (f"{target.name} perdeu um pouco da força dos golpes!")


def itemLogic(player, item, target, victory):
        if item.hp:
            oldHp = player.hp
            newHp = item.value + oldHp
            
            if oldHp == 100:
                return True, "Não irá ter efeito"
            
            if newHp > 100:
                hp_gain = 100 - oldHp
                player.hp = 100
            else:
                hp_gain = item.value 
                player.hp += hp_gain    

            print(f"{player.name} usou {item.name}!")
            return False, (f"{player.name} encheu {hp_gain:.0f} do seu HP")

        if item.status == "desparalyze":

            if player.status == "paralyzed":
                player.status = None
                player.speed = player.baseSpd
                print(f"{player.name} usou {item.name}!")
                
                return False, f"{player.name} curou paralisia!"
                #debug = True
            else:
                return True, "Não irá ter efeito"

        if item.pokeball:
            
            capturable = target.captureRate()
            print(f"{player.name} usou a Pokebola!")
            if capturable:
                time.sleep(1)
                print(f"..")
                time.sleep(1)
                print(f"...")
                time.sleep(1)
                victory = True
                return False, (f"Parabéns você capturou um {target.name}!!")
                time.sleep(2)
            
            else: 
                time.sleep(1)
                print(f"..")
                time.sleep(1)
                print(f"...")
                time.sleep(1)
                return False, ("Ah não! pensei ter capturado!")
            
def itemCount(player, item):
    item.amount -= 1
    if item.amount == 0:
        player.bagslot.remove(item)
    return ""

        


