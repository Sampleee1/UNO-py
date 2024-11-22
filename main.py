import os
import time
import random

dificuldade = ""


class Cartas:
    def __init__(self, cor, valor, tipo=None):
        self.cor = cor
        self.valor = valor
        self.tipo = tipo

    def __str__(self):
        if self.tipo == "normal":
            return f"{self.valor} ({self.cor})"
        elif self.tipo == "especial":
            return f"{self.valor} ({self.cor}, Especial)"
        elif self.tipo == "coringa":
            return f"{self.valor} (Coringa)"
        return "Carta desconhecida"


def LimpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')


def verificacao():

    while True:
        global inicio
        if inicio not in ["1", "2", "3", "4"]:
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
    (4) Sair
        
    ==> """))
    verificacao()

def opcoes():
    global inicio
    if inicio == "1": FuncaoUm()
    elif inicio == "2": FuncaoDois()
    elif inicio == "3": FuncaoTres()
    elif inicio == "4": print("Adeus!"); time.sleep(1)   
    
def criar_baralho():
    cores = ["Azul", "Verde", "Amarelo", "Vermelho"]
    valores = list(range(0, 10)) + ["+2", "Bloqueio", "Reverso"]
    baralho = []

    for cor in cores:
        for valor in valores:
            if isinstance(valor, int):
                tipo = "Normal"
            else:
                tipo = "Especial"
            temp = Cartas()
            if temp.tipo == "Especial":
                baralho.append(Cartas(cor, valor, tipo))
            baralho.append(Cartas(cor, valor, tipo))

    for _ in range(4):
        baralho.append(Cartas(None, "+4", "Coringa"))
        baralho.append(Cartas(None, "Trocar a cor", "Coringa"))
    return baralho



def FuncaoDois():
    print("Link do PDF das regras: https://www.bauru.unesp.br/Home/Div.Tec.Biblioteca/bd-manual-uno.pdf")
    time.sleep(1)
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


def FuncaoUm():
    LimpaTela()

    baralho = criar_baralho()
    random.shuffle(baralho)

    for carta in baralho[:5]:
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
    (2) Ver regras
    (3) Selecionar dificuldade
    (4) Sair

    ==> """)))

verificacao()

