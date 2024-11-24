import os
import time
import random
import webbrowser

dificuldade = ""

def Salva_rancking(nome,dificuldade):
    #abre um arquivo para armazenar o nome dos jogadores 
    rank = open ("Ranking.txt","r+")
    #for linha in rank.readlines():



    #variaveis gravados no arquigo
    nome=f"{nome}"
    nivel=f"{dificuldade}"
    resultado=""

    #monta a linha para ser gravada 
    linha =f"{nome}#{nivel}#{resultado}\n"
    #faz a gravação
    rank.write(linha)
    
    rank.close()

def FuncaoCinco():
    global n_jogador
    n_jogador= input(str("digite o nome do jogador: "))
    #Salva_rancking(n_jogador,dificuldade)    
    LimpaTela()
    caminhos()
    return(n_jogador)

class Cartas:
    def __init__(self, cor, valor, tipo=None):
        self.cor = cor
        self.valor = valor
        self.tipo = tipo

    def __str__(self):
        if self.tipo == "Normal":
            return f"{self.valor} ({self.cor})"
        elif self.tipo == "Especial":
            return f"{self.valor} ({self.cor}, Especial)"
        elif self.tipo == "Coringa":
            return f"{self.valor} (Coringa)"
        return "Carta desconhecida"


def LimpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')


def verificacao():

    while True:
        global inicio
        if inicio not in ["1", "2", "3", "4","5"]:
            inicio = input(str("""Opção invalida, digite novamente! 
    ==> """)) 
        else: 
            LimpaTela()
            opcoes()
            break


def caminhos():
    global inicio
    inicio = input(str("""
    -------------------------------------
    O que deseja fazer?
    (1) Jogar
    (2) Ver regras
    (3) Selecionar dificuldade
    (5) entrar com nome jogador
    (4) Sair
        
    ==> """))
    verificacao()

def opcoes():
    global inicio
    if inicio == "1": FuncaoUm()
    elif inicio == "2": FuncaoDois()
    elif inicio == "3": FuncaoTres()
    elif inicio == "5": FuncaoCinco()
    elif inicio == "4": print("Adeus!"); time.sleep(1)   
    
def criar_baralho():
    cores = ["Azul", "Verde", "Amarelo", "Vermelho"]
    valores = list(range(0, 10)) + ["+2", "Bloqueio", "Reverso"]
    baralho = []

    for cor in cores:                                            # Criação do primeiro baralho
        for valor in valores:
            if isinstance(valor, int):
                tipo = "Normal"
            else:
                tipo = "Especial"
                baralho.append(Cartas(cor, valor, tipo))
            baralho.append(Cartas(cor, valor, tipo))
    
    for carta in baralho[:63]:                                    # Criação do "Segundo Baralho"
        if carta.valor != 0 and carta.tipo != "Especial":
            baralho.append(carta)

    for _ in range(4):
        baralho.append(Cartas(None, "+4", "Coringa"))            # Criação das Coringas
        baralho.append(Cartas(None, "Trocar a cor", "Coringa"))
    return baralho



def FuncaoDois():
    url = "https://www.bauru.unesp.br/Home/Div.Tec.Biblioteca/bd-manual-uno.pdf"
    webbrowser.open_new_tab(url)

    caminhos()

def FuncaoTres():
    global dificuldade
    while True:
        LimpaTela()
        dificuldade = input(str("""
    Selecione a dificuldade:
            
    (1) Facil      (O bot esta muito azarado hoje e vai pegar as piores cartas.)
    (2) Medio      (Modo de jogo normal, chance padrao de pegar cada carta)
    (3) Dificil    (O bot esta com muita sorte hoje e vai fazer de tudo pra voce perder.)
    (4)  ...       (Apenas nao perca)
            
    ==> """))
        if dificuldade in ["1", "2", "3", "4"]:
            print(f"Dificuldade selecionada: {dificuldade}")
            time.sleep(1)
            caminhos()
            break
        else: print("Opção invalida, tente novamente"); time.sleep(1)
    #Salva_rancking(dificuldade)
    return(dificuldade)


def FuncaoUm():
    LimpaTela()

    baralho = criar_baralho()
    random.shuffle(baralho)

    for carta in baralho:
        print(carta)

inicio = input(str((""" 
              _____                    _____                   _______         
             /\    \                  /\    \                 /::\    \        
            /::\____\                /::\____\               /::::\    \       
           /:::/    /               /::::|   |              /::::::\    \      
          /:::/    /               /:::::|   |             /::::::::\    \     
         /:::/    /               /::::::|   |            /:::/~~\:::\    \    
        /:::/    /               /:::/|::|   |           /:::/    \:::\    \   
       /:::/    /               /:::/ |::|   |          /:::/    / \:::\    \  
      /:::/    /      _____    /:::/  |::|   | _____   /:::/____/   \:::\____\ 
     /:::/____/      /\    \  /:::/   |::|   |/\    \ |:::|    |     |:::|    |
    |:::|    /      /::\____\/:: /    |::|   /::\____\|:::|____|     |:::|    |
    |:::|____\     /:::/    /\::/    /|::|  /:::/    / \:::\    \   /:::/    / 
     \:::\    \   /:::/    /  \/____/ |::| /:::/    /   \:::\    \ /:::/    /  
      \:::\    \ /:::/    /           |::|/:::/    /     \:::\    /:::/    /   
       \:::\    /:::/    /            |::::::/    /       \:::\__/:::/    /    
        \:::\__/:::/    /             |:::::/    /         \::::::::/    /     
         \::::::::/    /              |::::/    /           \::::::/    /      
          \::::::/    /               /:::/    /             \::::/    /       
           \::::/    /               /:::/    /               \::/____/        
            \::/____/                \::/    /                 ~~              
             ~~                       \/____/                                         
    -----------------------------------------------------------------------------
    Seja bem-vindo ao UNO, desenvolvido por Fred Luis, Nata Ramos e Miguel Yoshida. :)

    O que deseja fazer?
    (1) Jogar
    (2) Ver regras (Vai abrir o navegador)
    (3) Selecionar dificuldade
    (5) Inserir nome do jogador
    (4) Sair

    ==> """)))

verificacao()

