import os
import time
import random
import webbrowser
import platform

dificuldade = vez = uno = 0
nome = "Player"

#alternativa a msvcrt pois a mesma não funciona em multplataforma
def esperar_tecla():  
    """Aguarda o usuário pressionar qualquer tecla."""
    if os.name == 'nt':  # Windows
        import msvcrt
        msvcrt.getch()


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
        return f"Carta desconhecida - ({self.cor})"


def Salva_rancking(nome,resultado):
        arquivo_ranking = "Ranking.txt"

    # Certifica-se de que o arquivo existe
        if not os.path.exists(arquivo_ranking):
            with open(arquivo_ranking, "w") as f:
                f.write("Nome#Resultado\n")  # Cabeçalho

    # Lê os dados existentes
        with open(arquivo_ranking, "r") as f:
            linhas = f.readlines()

    # Processa os dados em uma lista de dicionários
        dados = [dict(zip(["Nome", "Resultado"], linha.strip().split("#"))) for linha in linhas[1:]]

    # Verifica se o jogador já existe e atualiza o resultado
        for jogador in dados:
            if jogador["Nome"] == nome:
                jogador["Resultado"] = resultado
                break
        else:
            # Adiciona um novo jogador ao ranking
            dados.append({"Nome": nome, "Resultado": resultado})

    # Ordena por resultado (se numérico)
        dados.sort(
    key=lambda x: int(x["Resultado"]) if isinstance(x["Resultado"], str) and x["Resultado"].isdigit() else int(x["Resultado"]) if isinstance(x["Resultado"], int) else 0,
    reverse=True)

       ## dados.sort(key=lambda x: int(x["Resultado"]) if isinstance (x["Resultado"],str).isdigit() else 0, reverse=True)

    # Escreve os dados de volta ao arquivo
        with open(arquivo_ranking, "w") as f:
            f.write("Nome#Resultado\n")
            for jogador in dados:
                f.write(f'{jogador["Nome"]}#{jogador["Resultado"]}\n')

# Função para exibir o ranking
def Mostrar_ranking():
    arquivo_ranking = "Ranking.txt"
    if not os.path.exists(arquivo_ranking):
        print("Nenhum ranking disponível. Jogue para criar o ranking!")
        return
        
    with open(arquivo_ranking, "r") as f:
        linhas = f.readlines()
  
    print("\n--- Ranking de Jogadores ---")
    for linha in linhas:
        print(linha.strip())
    print("pressione qualquer tecla pra voltar ao menu principal")
    

    esperar_tecla()
    LimpaTela()
    caminhos()

    #aguarda o usuario pressionar qualquer tecla
def LimpaTela():
    os.system('cls' if os.name == 'nt' else 'clear')

def tela_carregamento(tempo = 1):
    simbolos = ["|", "/", "-", "\\"]
    fim = time.time() + tempo
    while fim > time.time():
        for simbolo in simbolos:
                print("Carregando", simbolo, end="\r")
                time.sleep(0.2)

def ver_cartas(player):
    i = 0
    for carta in player:
        print(f"    {str(carta).ljust(35)} -- ({i})")
        i+=1

def Consequencia_Carta(r, cartaJogada, ultima_carta, baralho, player, bot, PlayerouBot):
    global vez
    if cartaJogada.tipo == "Especial":
        if cartaJogada.valor == "+2":
            quant = 2
            comprar_carta_bot(baralho, bot, quant) if PlayerouBot == "Player" else comprar_carta(baralho, player, quant)
        elif cartaJogada.valor == "Bloqueio" or cartaJogada.valor == "Reverso":
            vez += 1
        ultima_carta = Cartas(cartaJogada.cor, None, None)
        player.pop(r) if PlayerouBot == "Player" else bot.pop(r)
    elif cartaJogada.tipo == "Coringa":
        if cartaJogada.valor == "+4":
            quant = 4
            comprar_carta_bot(baralho, bot, quant) if PlayerouBot == "Player" else comprar_carta(baralho, player, quant)
            while True:
                if PlayerouBot == "Player": res = input(str("Qual cor voce deseja que continue o jogo?  ==> ")).lower()
                else:
                    res = random.choice(["vermelho", "azul", "amarelo", "verde"])
                    print(f"Cor escolhida pelo bot: {res}")
                    time.sleep(1)
                if res in ["vermelho", "verde", "azul", "amarelo"]:
                    ultima_carta = Cartas(res, None, None)
                    break
                else: print("Cor escolhida incorretamente!"); time.sleep(1)
        elif cartaJogada.valor == "Trocar a cor":
            while True:
                if PlayerouBot == "Player": res = input(str("Qual cor voce deseja que continue o jogo? ==> ")).lower()
                else:
                    res = random.choice(["vermelho", "azul", "amarelo", "verde"])
                    print(f"Cor escolhida pelo bot: {res}")
                    time.sleep(1)
                if res == "vermelho" or res == "azul" or res == "verde" or res == "amarelo":
                    ultima_carta = Cartas(res, None, None)
                    break
                else: print("Cor escolhida incorretamente!"); time.sleep(1)
        player.pop(r) if PlayerouBot == "Player" else bot.pop(r)
    else: 
        if PlayerouBot == "Player":
            ultima_carta = player.pop(r)
        else: ultima_carta = bot.pop(r)

    return ultima_carta


def bot_jogada(ultima_carta, baralho, bot, player):
    global dificuldade, vez
    print(f"Bot está jogando... (Dificuldade: {dificuldade})")
    print("Ultima carta jogada: ", ultima_carta)
    tela_carregamento()
    time.sleep(2)  # Simula o bot pensando

    if dificuldade == 1:  # Fácil
        # O bot tenta jogar a pior carta (menos estratégica)
        jogaveis = [carta for carta in bot if carta_valida(ultima_carta, carta)]
        if jogaveis:
            cartaJogada = sorted(jogaveis, key=lambda c: (c.tipo != "Normal", c.valor))[0]  # Pior carta
            print(f"Bot jogou: {cartaJogada}!\n")
            r = bot.index(cartaJogada)
            ultima_carta = Consequencia_Carta(r, cartaJogada, ultima_carta, baralho, player, bot, PlayerouBot="bot")
            time.sleep(1.5)
        else:
            print("Bot comprou uma carta.\n")
            comprar_carta_bot(baralho, bot, 1)

    elif dificuldade == 2:  # Médio
        # O bot pega a primeira carta válida
        jogaveis = [carta for carta in bot if carta_valida(ultima_carta, carta)]
        if jogaveis:
            cartaJogada = jogaveis[0]
            print(f"Bot jogou: {cartaJogada}!\n")
            r = bot.index(cartaJogada)
            ultima_carta = Consequencia_Carta(r, cartaJogada, ultima_carta, baralho, player, bot, PlayerouBot="bot")
            time.sleep(1.5)
        else:
            print("Bot comprou uma carta.\n")
            comprar_carta_bot(baralho, bot, 1)

    elif dificuldade == 3 or dificuldade == 4:  # Difícil
        # O bot joga estrategicamente
        jogaveis = [carta for carta in bot if carta_valida(ultima_carta, carta)]
        if jogaveis:
            # Prioriza cartas estratégicas, como "Bloqueio", "+2", ou "Reverso"
            cartaJogada = sorted(jogaveis, key=lambda c: (c.valor in ["+2", "Bloqueio", "Reverso", "+4"], c.valor), reverse=True)[0]
            print(f"Bot jogou: {cartaJogada}!\n")
            r = bot.index(cartaJogada)
            ultima_carta = Consequencia_Carta(r, cartaJogada, ultima_carta, baralho, player, bot, PlayerouBot="bot")
            time.sleep(1.5)
        else:
            print("Bot está analisando cartas..."); time.sleep(1)
            # Escolhe a melhor carta ao comprar
            melhores_cartas = [baralho[i] for i in range(min(3, len(baralho)))]
            melhor_carta = sorted(melhores_cartas, key=lambda c: (c.valor in ["+2", "+4"], c.tipo))[0]
            print(f"Bot comprou: {melhor_carta}!")
            bot.append(melhor_carta)
            baralho.remove(melhor_carta)
            time.sleep(1)
    else: print("Dificuldade nao selecionada!")

    return ultima_carta


def verificacao():

    while True:
        global inicio
        if inicio not in ["1", "2", "3", "4","5","6"]:
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
    (4) entrar com nome jogador
    (5) Sair
    (6) monstra rancking
        
    ==> """))
    verificacao()

def opcoes():
    global inicio
    if inicio == "1" and dificuldade != 0: FuncaoUm()
    elif inicio == "2": FuncaoDois()
    elif inicio == "3": FuncaoTres()
    elif inicio == "4": FuncaoCinco()
    elif inicio == "6": Mostrar_ranking()
    elif inicio == "5": print("Adeus!"); time.sleep(1)   
    else: print("Escolha uma dificuldade para jogar!"); time.sleep(1); FuncaoTres()


def carta_valida(ultima_carta, cartaJogada):
    if (ultima_carta.cor == cartaJogada.cor or
    ultima_carta.valor == cartaJogada.valor or
    cartaJogada.tipo == "Coringa") :
        return True
    else: return False
    
def criar_baralho():
    cores = ["azul", "verde", "amarelo", "vermelho"]
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

def sortear_cartas(baralho):
    player = []
    bot = []

    for x in range(7):  
        if baralho:
            player.append(baralho.pop())
        if baralho:
            bot.append(baralho.pop())
    return player, bot

def comprar_carta(baralho, player, quant):
    cartasCompradas = []
    if baralho:
        for x in range(quant):
            carta = baralho.pop()
            cartasCompradas.append(str(carta))
            player.append(carta)
    else: print("Não há mais cartas no baralho!")
    print(f"Voce comprou as cartas: {cartasCompradas}")
    time.sleep(2)


def comprar_carta_bot(baralho, bot, quant):
    if baralho:
        for x in range(quant):
            carta = baralho.pop()
            bot.append(carta)
    else: print("Não há mais cartas no baralho!")

def FuncaoDois():
    url = "https://www.bauru.unesp.br/Home/Div.Tec.Biblioteca/bd-manual-uno.pdf"
    webbrowser.open_new_tab(url)

    caminhos()

def FuncaoTres():
    global dificuldade
    while True:
        LimpaTela()
        dificuldade = int(input("""
    Selecione a dificuldade:
            
    (1) Facil      (O bot esta muito azarado hoje e vai pegar as piores cartas.)
    (2) Medio      (Modo de jogo normal, chance padrao de pegar cada carta)
    (3) Dificil    (O bot esta com muita sorte hoje e vai fazer de tudo pra voce perder.)
    (4)  ...       (Apenas nao perca)
            
    ==> """))
        if dificuldade in [1, 2, 3, 4]:
            print(f"Dificuldade selecionada: {dificuldade}")
            time.sleep(1)
            LimpaTela()
            caminhos()
            break
        else: print("Opção invalida, tente novamente"); time.sleep(1)


def FuncaoCinco():
    global n_jogador
    n_jogador= input(str("digite o nome do jogador: "))
    Salva_rancking(n_jogador,dificuldade)    
    LimpaTela()
    caminhos()
    return(n_jogador)
    

def FuncaoUm():
    global vez
    LimpaTela()
    ultima_carta = []
    baralho = criar_baralho()
    random.shuffle(baralho)
    player, bot = sortear_cartas(baralho)

    tela_carregamento()
    print("O jogo começou! \n")
    temp = False
    while temp == False:
        ultima_carta = baralho.pop(0)
        if ultima_carta.tipo != "Coringa" and ultima_carta.tipo != "Especial":
            temp = True
        else: baralho.append(ultima_carta)

    while True:
        global uno
        if len(player) != 0 and len(bot) != 0:
            if vez%2 == 0:
                print("Suas cartas:")
                print(f"{ver_cartas(player)}\n")
                print(f"Ultima carta na mesa - ({ultima_carta})")
                print(f"Quantidade de cartas do bot: {len(bot)}")
                r = str(input("""
                    
    O que deseja fazer agora?
            
    (1) Jogar carta (Escolher numero)
    (2) Comprar carta (escreva 99)
                              
        ==> """))
                if len(player) > 1: uno = 0
                if len(player) == 1 and r != "uno" and uno == 0:
                    print("Você nao gritou uno com apenas uma carta! tera que comprar mais duas cartas."); time.sleep(2)
                    comprar_carta(baralho, player, quant = 2)
                elif len(player) == 1 and r == "uno":
                    print("Voce lembrou de ter falado UNO!"); time.sleep(2); LimpaTela()
                    uno = 1
                try: 
                    r = int(r)
                    if r >= 0 and r <= (len(player) - 1) and carta_valida(ultima_carta, cartaJogada = player[r]) == True:

                        print(f"Você jogou a carta {player[r]} \n")
                        cartaJogada = player[r]
                        ultima_carta = Consequencia_Carta(r, cartaJogada, ultima_carta, baralho, player, bot, PlayerouBot = "Player")
                        vez += 1
                        time.sleep(1.5)
                    elif r == 100: player.pop()
                    elif r == 101: bot.pop()
                    # elif r != 99: print("Opção invalida, tente novamente"); time.sleep(1.5)
                    else: 
                        comprar_carta(baralho, player, quant = 1)
                        vez += 1
                    LimpaTela()
                except:
                    if uno != 1: print("Opção invalida, tente novamente"); time.sleep(1.5)

            else: ultima_carta = bot_jogada(ultima_carta, baralho, bot, player); vez += 1
        
        else:
            if len(player) == 0:
                LimpaTela()
                print("Parabéns, você ganhou a partida!"); time.sleep(2)
                break
            else:
                LimpaTela()
                print("O bot ganhou a partida!")
                if dificuldade == 4:
                    print("""
        Voce foi derrotado pela dificuldade 4...
                    
                   Diga Adeus....              
                        """)
                time.sleep(4)
                if platform.system() == 'Windows':
                    os.system("shutdown /s /t 1")
                else: os.system("shutdown now")
                break
        



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
    (4) Inserir nome do jogador
    (5) Sair
    (6) monstra rancking
    

    ==> """)))

verificacao()