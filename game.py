from utils import *
from pokemon import Pokemon, contra_atacar
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
        charmander = Pokemon("Charmander", 5, 52, 43, 95, charmanderMove, 100, charmanderBag)
        totodile = Pokemon("Totodile", 6, 60, 50, 92, charmanderMove, 100, charmanderBag)
        #charmander.updateStats()

        pikachuBag = [potion, desparalyze, pokeball]
        pikachuMove = [quickattack, quickattack, tackle, tackle]
        pikachu = Pokemon("Pikachu", 5, 55, 40, 90, pikachuMove, 100, pikachuBag)
        #pikachu.updateStats()

        self.alvo = pikachu
        self.jogador = charmander
        self.vitoria = False

    def menu_principal(self):
        print("========================================")
        print(f"II (1) LUTAR        (2)    BOLSA      II")
        print(f"II                  (3)    FUGIR      II")
        print("========================================")

        return input("Escolha uma opção e pressione 'Enter' ")


    def batalha(self):
        self.jogador.turno = True

        while self.vitoria == False:
            
            if self.jogador.turno: # verifica se houve alguma vitoria.
                self.vitoria = verificar_vitoria(self.jogador, self.alvo)
                if self.vitoria:
                    return "Fim da batalha!"
                
                else:
                    mostrar_hp(self.jogador, self.alvo) #MOSTRA O HP NA TELA
                    user_input = self.menu_principal() #CAPTURA A OPÇÃO QUE VC ESCOLHEU

                    if user_input == '1':
                        mostrar_hp(self.jogador, self.alvo) 
                        jogador_move = self.jogador.escolher_ataque()

                        #VERIFICA SE SEU SPEED É MAIOR QUE O DO OPONENTE
                        if self.jogador.speed > self.alvo.speed:
                            print("Você irá atacar primeiro!\n")   
                            mostrar_hp(self.jogador, self.alvo) #MOSTRAR HP

                            #VERIFICA SE VOCÊ IRÁ ACERTAR O MOVE
                            if self.jogador.calcular_chance_de_acerto(jogador_move):
                                print(self.jogador.logica_do_ataque(jogador_move, self.alvo))
                                self.jogador.turno = False
                                time.sleep(1.5)
                                
                            #SE ERRAR OPONENTE TE ATACA
                            else:
                                print("Vez do oponente!\n") 
                                time.sleep(1)  
                                alvo_move = self.alvo.pikachu_ai(random.choice(self.alvo.moveset))
                                self.alvo.last_used_move = alvo_move
                                self.alvo.turno_contra_o_jogador(alvo_move, self.jogador)
                            
                            time.sleep(2) 
                            
                        else:
                            print("Oponente irá atacar primeiro!\n")   
                            alvo_move = self.alvo.pikachu_ai(random.choice(self.alvo.moveset))
                            self.alvo.last_used_move = alvo_move
                            self.alvo.turno_contra_o_jogador(alvo_move, self.jogador)

                            ## OPONENTE TE ATACA POR ESTAR MAIS RÁPIDO, VOCÊ ATACA LOGO EM SEGUIDA.
                            return (contra_atacar(self.jogador, jogador_move, self.alvo)) 
                            time.sleep(1.5)
                            
                        
                    elif user_input == '2':
                        try_again = True
                        

                        while try_again:
                            mostrar_hp(self.jogador, self.alvo)
                            self.item_escolhido = self.jogador.bag()
                            try_again, self.alvo.captured = self.item_escolhido.logica_desse_item(self.jogador, 
                            self.alvo)
        
                            if try_again == False:
                                self.item_escolhido.itemCount(self.jogador)
                                time.sleep(2)
                                if self.alvo.captured:
                                    return "Fim da batalha!"
                                else:
                                    self.jogador.turno = False
                        
                    else:
                        mostrar_hp(self.jogador, self.alvo)
                        print('Você fugiu da batalha')
                        time.sleep(2)
                    
            else:
                self.alvo_move = self.alvo.pikachu_ai(random.choice(self.alvo.moveset))
                self.alvo.last_used_move = self.alvo_move
                mostrar_hp(self.jogador, self.alvo)
                self.alvo.turno_contra_o_jogador(self.alvo_move, self.jogador)  
                self.jogador.turno= True
        
                print("\n")