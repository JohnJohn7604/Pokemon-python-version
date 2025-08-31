import random, time, os

def verificar_vitoria(jogador, alvo):
        if jogador.hp <= 1:
            print(f"{jogador.name} desmaiou!")
            return True
        elif alvo.hp <= 1:
            print(f"{alvo.name} desmaiou!")
            return True
        else:
            return False
    
def limpa_tela():
    return os.system('cls' if os.name == 'nt' else 'clear') #se for windows limpa com o 'cls' senao o 'clear'

def mostrar_hp(jogador, alvo):
    
    limpa_tela()
    print("========Inimigo=======")
    print(f"II   {alvo.name} Lvl. {alvo.lvl} II")
    print(f"II   HP: {alvo.hp:<10.0f} II")   
    print("======================")  

    print("              ==========Você==========")
    print(f"              II  {jogador.name} Lvl. {jogador.lvl:<1} II")
    print(f"              II  HP: {jogador.hp:<14.0f}II")   
    print("              ========================") 


        


