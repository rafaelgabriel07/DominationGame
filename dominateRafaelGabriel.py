#Aluno: Rafael Magalhaes de Matos Gabriel

import time as tm
import os


def imprimirTab(tabuleiro):                 #Criei essa funcao com o intuito de a cada
    nLin = 1                                #rodada, mostrar o tabuleiro do jogo para os
    for linha in tabuleiro:                 #jogadores. Nela, eu transformava cada linha
        l = str(linha)[1:-1]                #da lista em uma string e no final, colocava
        l = l.split(', ')                   #as coordenadas das colunas
        strL = ''
        for pos in l:
            if pos == "'X'":    #Tive que separar em dois casos pois se colocasse para imprimir o X da mesma maneira que os outros numero o tabuleiro ficava estranho
                strL = strL + pos[1:2] + ' '
            else:
                strL = strL + pos + ' '
        strL = strL + ' -' + str(nLin)
        nLin = nLin + 1
        print(strL)
    print('| | | | | | | |')
    print('1 2 3 4 5 6 7 8')
        

def verPos(tabuleiro,lin,col,jog):                         
    if (lin != '1' and lin != '2' and lin != '3' and\
        lin != '4' and lin != '5' and lin != '6' and\
        lin != '7' and lin != '8') or\
        (col != '1' and col != '2' and col != '3' and\
        col != '4' and col != '5' and col != '6' and\
        col != '7' and col != '8'):    #Aqui va haver a verificação de se for uma entrada em que possa ser um possível movimento
        return 0
    else:                                  #Se for um número válida ela, a função vai transfomar a string do número em um inteiro
        lin = int(lin)
        col = int(col)
        if tabuleiro[lin-1][col-1] != 0 and tabuleiro[lin-1][col-1] != 'X':   #Aqui, vai ver se a casa selecionada é válida, ou seja,
            return 0                       #se a casa selecionada não está ocupada por outro número 
        else:                              #(lembrando que como o tabuleiro é uma lista, a linha ou coluna x vai ser a posição x-1 na lista)
            for x in range(-2,1):          #Aqui vai verificar se foi realizado um movimento para uma casa adjacente
                for y in range(-2,1):      #Esses dois "for" faz a verificação de todas as casas adjacentes
                    try:
                        if col+y<0 or col+y>7 or lin+x<0 or lin+x>7:
                            raise IndexError            #O raise index aqui é para situações em que a soma da um número negativo, 
                        pos = tabuleiro[lin+x][col+y]   #pois quando for procurar a posição com esse número ela vai pegar a lista de traz para frente, e não é isso que eu quero
                    except IndexError:
                        pass
                    else:
                        if pos == jog:
                            return 1
            for x in [-3,-1,1]:      #Se não for encontrado nenhuma casa adjacente com um número para poder andar,
                for y in [-3,-1,1]:  #agora a função vai ver se foi realizado um salto
                    if (x == -3 and y == -3) or (x == -3 and y == 1) or\
                       (x == 1 and y == -3) or (x == 1 and y == 1):
                        continue  #Essa condicional serve para não testar saltos que não são permitidos
                    try:
                        if lin+x<0 or lin+x>7 or col+y<0 or col+y>7:
                            raise IndexError  #Esse raise é pelo mesmo motivo do explicado em cima
                        pos = tabuleiro[lin+x][col+y]
                    except IndexError:
                        pass
                    else:
                        if pos == jog:
                            return 2
    return 0  #Se mesmo sendo uma coordenada válida, ou seja, o input da linha e coluna são números
              #e o número na casa nessa coordenada for 0, é possível que não seja um movimento válido
              #Então ser não foi um salto ou um movimento para uma casa adjacente, isso quer dizer que 
              #foi selecionada uma casa inválida, retornando 0


def verPossivelContinuar(tabuleiro,jog):                 #Essa função vai ser chamada sempre antes de um jogador fazer o movimento
    for posLinha in range(8):               #Ela serve pra verificar se é possível para um jogador realizar algum movimento
        for posColuna in range(8):           #Ela retorna 1 se for possível e 0 se não for possível
            coordenada = tabuleiro[posLinha][posColuna]
            if coordenada == jog:
                for x in range(-1,2):
                    for y in range(-1,2):
                        try:
                            if (posLinha+x<0 or posLinha+x>7) or (posColuna+y<0 or posColuna+y>7):
                                raise IndexError    #Raise com o mesmo motivo dos outros já vistos
                            pos = tabuleiro[posLinha+x][posColuna+y]
                        except IndexError:
                            pass
                        else:
                            if pos == 0:
                                return 1
                for x in [-2,0,2]:
                    for y in [-2,0,2]:
                        if (x == -2 and y == -2) or (x == -2 and y == 2) or\
                           (x == 2 and y == -2) or (x == 2 and y == 2) or (x == 0 and y == 0):
                            continue
                        try:
                            if (posLinha+x<0 or posLinha+x>7) or (posColuna+y<0 or posColuna+y>7):
                                raise IndexError
                            salto = tabuleiro[posLinha+x][posColuna+y]
                        except IndexError:
                            continue
                        else:
                            if salto == 0:
                                return 1
                
    return 0


def alterarDadosJogs(dJ):   #Essa função vai escrever os dados de cada jogador em um arquivo txt(dJ é uma lista com os dados do jogador na partida)
    try:  #Aqui vai tentar abrir o arquivo que está com os dados dos jogadores
        dados = open('DadosJogs.txt','r')
    except FileNotFoundError:
        dados = open('DadosJogs.txt','a') #Se não existir esse arquivo, a função vai criar o arquivo 
        for x in dJ:      #E aqui ela vai colocar os dados do jogador no arquivo
            dados.write(str(x)) #Lembrando, a ordem vai ser sempre:
            dados.write(',')    #Nome,1(pra indicar que foi jogado uma partida),1 ou 0(se ganhar ou perder a partida respectivamente),maior pontuação,maior tempo,menor tempo , 
        dados.write('\n')
        dados.close()
    else: #Se o arquivo já existir, ela vai reescrever esse arquivo adicionando os novos dados nele
        linhas = dados.readlines()
        dados.close()
        dados = open('DadosJogs.txt','w')
        igual = 0  #Essa variável vai indicar se já existe algum dado do jogador dentro do arquio de texto(0 se não e 1 se tem)
        for x in linhas:  #Aqui, vai ocorrer a transformação de uma linha daquele arquivo de texto em uma lista
            lista = x[:-2]
            lista = lista.split(',')
            if lista[0] == dJ[0]:    #Se o nome daquela linha for igual ao da lista de entrada:
                igual = 1    #O a variavel vai mudar para 1 indicando que já existe dados do jogador na lista
                dados.write(lista[0])    #Vai colocar o nome do jogador
                dados.write(',')
                dados.write(str(int(lista[1])+int(dJ[1])))    #Aqui vai somar o número de partidas anteriores mais o 1 do dj indicando que foi jogado mais uma partida
                dados.write(',')
                dados.write(str(int(lista[2])+int(dJ[2])))    #Aqui vai somar para indicar o número de vitórias
                dados.write(',')
                if int(lista[3]) >= int(dJ[3]):    #Essa condicional vai ver se a pontuação que estava no arquivo antes é maior do que a obtida na última partida
                    dados.write(str(lista[3]))     #Se for maior ela mantem a do arquivo e se for menor ela substitui pelo da lista dJ
                else:
                    dados.write(str(dJ[3]))
                dados.write(',')
                if float(lista[4]) >= float(dJ[4]):    #Mesma coisa que a de cima só que para verificar o tempo
                    dados.write(str(lista[4]))
                else:
                    dados.write(str(dJ[4]))
                dados.write(',')
                if float(lista[5]) >= float(dJ[5]):    #Também a mesma coisa, porém para verificar o menor tempo
                    dados.write(str(dJ[5]))
                else:
                    dados.write(str(lista[5]))
                dados.write(',')
                dados.write('\n')
            else:
                for x in lista:    #Se os nomes forem diferentes, ele só adiciona de novo aquelas informações no arquivo
                    dados.write(str(x))
                    dados.write(',')
                dados.write('\n')
        if igual == 0:    #Aqui vai entrar aquela variável. Se em nenhum momento ela mudou para 1, isso indica que é um jogador novo, então só adiciona as informações dele no arquivo
            for x in dJ:
                dados.write(str(x))
                dados.write(',')
            dados.write('\n')
                
        dados.close()


def historico(dadosPartida):    #Essa função ser para adicionar as informações da partida jogada em um arquivo de texto
    dados = open('DadosPartida.txt','a')    #As informações são:G ou E(indicando que há um ganhador ou foi empate respectivamente)
    for x in dadosPartida:                  #Ganhador,perdedor,pontuação ganhador,pontuação perdedor,tempo de partida
        dados.write(str(x))
        dados.write(',')
    dados.write('\n')
    dados.close()


def preencherTab(tab):    #Essa vai ser a função que completa o tabuleiro se ainda há possibilidade depois do fim do jogo
    for posLinha in range(8):
        for posColuna in range(8):
            if tab[posLinha][posColuna] == 0:    #Quando ela encontrada uma casa que há um 0, ela vai verificar ao redor se há algum 1 ou 2 para colocar naquela casa
                for x in range(-1,2):
                    for y in range(-1,2):
                        try:
                            casas = tab[posLinha+x][posColuna+y]
                        except IndexError:
                            continue
                        else:
                            if tab[posLinha+x][posColuna+y]:
                                tab[posLinha][posColuna] = tab[posLinha+x][posColuna+y]
    for linha in tab:    #Depois de passar por todo o tabuleiro ela vai verificar se ainda há 0
        for num in linha:    #Se houver, ela faz a chamada dela mesmo, até que não haja mais 0, retornando o novo tabuleiro
            if num == 0:
                tab = preencherTab(tab)
    return tab


def salvarJogo(j1,j2,tab,rodada,tempo,vezJogador):
    arq = open('Save.txt','w')    #Essa função vai salvar as informações do jogo em um arquivo para se os jogadores quiserem sair no meio de uma partida
    arq.write(j1)    #As informações são escrita no arquivo da seguinte maneira:
    arq.write('\n')  #Jog1\n Jog2\n linhaX(x variando de 1 a 8)\n \n(deixar uma linha vazia vai ser importante para depois) rodada\n tempo\n vezJog\n(indica de quem é a vez)
    arq.write(j2)
    arq.write('\n')
    for linha in tab:
        arq.write(str(linha))
        arq.write('\n')
    arq.write('\n')
    arq.write(str(rodada))
    arq.write('\n')
    arq.write(str(tempo))
    arq.write('\n')
    arq.write(str(vezJogador))
    arq.close()


def lerSave():    #Função responsável por carregar o jogo antigo
    save = open('Save.txt','r')    #Para isso ela vai ler o arquivo e atribui os valores a cada variável
    linha = save.readline()    #Por isso é importante a ordem, não só nesse arquivo mas em todos os outros
    j1 = linha[:-1]
    linha= save.readline()
    j2 = linha[:-1]
    linha = save.readline()
    tab = []
    while linha != '\n':    #O motivo daquele \n se importante é porque ele vai ser a condição de para para conseguir pegar o tabuleiro
        linha = linha[1:-2]
        linha = linha.split(',')
        for pos in range(8):
            linha[pos]=int(linha[pos])
        tab = tab+[linha]
        linha = save.readline()
    linha = save.readline()
    rodada = int(linha)
    linha = save.readline()
    tempo = float(linha)
    linha = save.readline()
    vezJogador = int(linha)
    save.close()
    return j1,j2,tab,rodada,tempo,vezJogador


def printPlacar(tab):    #Função responsável por contar quantos pontos cada jogador fez
    p1 = 0
    p2 = 0
    for linha in tab:    #Explicando de maneira simplificada, ela vai passar por cada casa e ver qual jogador ocupa ela
        for coluna in linha:    #Se for o jogador 1, somasse 1 na p1, e se for 2, somasse 1 na p2
            if coluna == 1:
                p1 = p1+1
            elif coluna == 2:
                p2 = p2+1
    print('Jogador 1: {} vs Jogador 2: {}'.format(p1,p2))    #Então no final, ele imprime na tela a pontuação
            
        
        
    

    
def dominate(arq):    #Essa é a principal função, a que vai rodar o jogo
    if arq == 0:    #Esse arq serve pra indicar como vai ser aberto o jogo. Se arq = 0 isso indica que está sendo iniciado um novo jogo
        j1 = input('Insira seu nome, Jogador 1: ')    #Se arq = 1, indica que existe um arquivo com save de um jogo anterior, então ele vai ler esse arquivo para atribuir os valores a cada variavel
        if j1.upper() == 'S':
            print('==========================')
            return 0,0,0    #Tanto nesse if quanto no if debaixo não chamei a função salvarJogo pois não tinha nada para ser salvo
        while True:    #Coloquei esse while aqui para enquanto o nome do jogador 2 for igual ao do jogador 1 o jogo não iniciar pois isso poderia acarretar em problemas futuros
            j2 = input('Insira seu nome, Jogador 2: ')
            if j2.upper() == 'S':
                print('==========================')
                return 0,0,0    #Sempre que o jogador quiser sair do jogo, a função vai retornar 0,0,0 e isso será importante no futuro
            if j2 == j1:
                print('Por favor, insira um nome diferente do jogador 1')
            else:
                break
        tab = [[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]]    #Tabuleiro inicial
        rodada = 1
        tempoAntes = 0    #Tanto a variavel tempoAntes e vezJogador são importantes para salvar o jogo pois:
        vezJogador = 1    #A variavel tempoAntes vai salvar o tempo de partida antes de salvar, para quando carregar novamente o jogo somar esse tempo com o novo tempo de jogo
        print('Que comecem o Jogos!')    #Já a vezJogador vai impedir de o jogo ser finalizado pelo jogador 2 e quando carregado o jogo recomeçar na vez do jogador 1
        print('Lembre-se: O Jogador so pode se mover para as casas onde ha um X')
        t0 = tm.time()    #Tempo de início da partida
        print('==========================')
    else:    #Aqui é o caso de arq = 1, atribuindo a cada variavel o valor do jogo anterior
        j1,j2,tab,rodada,tempoAntes,vezJogador = lerSave()
        print('Que comecem o Jogos!')
        print('Lembre-se: O Jogador so pode se mover para as casas onde ha um X')
        t0 = tm.time()
        print('==========================')
    while True:    #Esse while vai manter o jogo rodando até que seja impossível de continuar
        jogador = 1    #Essa variavel vai ser importante pois diversas funções pedem ela pra saber em qual vez tá
        verificacao = verPossivelContinuar(tab,jogador)    #A função já mencionada para ver se é possível ou não continuar
        if verificacao == 0:    #Se retornar 0, isso indica que é impossível continuar saindo então do while
            break
        print('Rodada: {}'.format(rodada))
        if vezJogador == 1:
            for lin in range(1,9):
                for col in range(1,9):
                    pos = verPos(tab,str(lin),str(col),jogador)
                    if pos == 1 or pos == 2:
                        tab[lin-1][col-1] = 'X'
            
            print('{}, seu turno!'.format(j1))
            print('==========================')
            printPlacar(tab)
            imprimirTab(tab)
            print('==========================')
            while True:    #Esse while vai manter o jogador preso até ele colocar as coordenadas de uma casa permitida ou sair do jogo
                lin = input('Selecione a linha desejada: ')
                col = input('Selecione a coluna desejada: ')
                if lin.upper() == 'S' or col.upper() == 'S':
                    for lin in range(8):
                        for col in range(8):
                            if tab[lin][col] == 'X':
                                tab[lin][col] = 0
                    vezJogador = 1
                    tf = tm.time()
                    salvarJogo(j1,j2,tab,rodada,tf-t0+tempoAntes,vezJogador)
                    print('==========================')
                    return 0,0,0
                res = verPos(tab,lin,col,jogador)    #Aqui ele chama aquela função para verificar e é possível ir para a casa selecionado e ver qual tipo de movimento foi realizado
                if res == 0:
                    print('Por favor, insira uma posicao valida.')
                elif res == 1:    #Como já foi dito, quando aquela função retorna 1, isso indica que o jogador foi para uma casa adjacente a alguma casa já dele
                    lin = int(lin)
                    col = int(col)
                    tab[lin-1][col-1] = 1    #Então, ele muda o valor da casa selecionada para 1 (lembrando que como já foi dito, para a linha ou coluna x, o acesso a ela se da por x-1, devido ao fato do tabuleiro ser uma lista)
                    for x in range(-2,1):    #A partir desse "for" até o "break" vai ser a parte responsável
                        for y in range(-2,1):#por mudar o valor das casas do adversário
                            try:
                                if (lin+x<0 or lin+x>7) or (col+y<0 or col+y>7):
                                    raise IndexError
                                pos = tab[lin+x][col+y]
                            except IndexError:
                                continue
                            else:
                                if pos == 2:
                                    tab[lin+x][col+y] = 1
                    break
                else:    #Se a função entrar nesse else, indica que o jogador realizou um salto
                    lin = int(lin)
                    col = int(col)
                    tab[lin-1][col-1] = 1
                    possiveisSaltos = 0    #Essa vai ser uma variável importante, mas por equanto vamos deixar de lado
                    for x in range(-2,1):
                        for y in range(-2,1):
                            try:
                                if (lin+x<0 or lin+x>7) or (col+y<0 or col+y>7):
                                    raise IndexError
                                pos = tab[lin+x][col+y]
                            except IndexError:
                                continue
                            else:
                                if pos == 2:
                                    tab[lin+x][col+y] = 1    #O procedimento até aqui é o mesmo anteriormente (ignorando aquela variável)
                    for x in [-3,-1,1]:    #A partir daqui as coisas mudam. Aqui a função vai verificar de qual casa foi realizado o salto para voltar o valor dessa casa para 0
                        for y in [-3,-1,1]:    #E aqui também é onde entra a variável possiveisSaltos
                            if (x == -3 and y == -3) or (x == -3 and y == 1) or\
                               (x == 1 and y == -3) or (x == 1 and y == 1) or (x == -1 and y == -1):
                                continue
                            try:
                                if lin+x<0 or lin+x>7 or col+y<0 or col+y>7:
                                    raise IndexError
                                pos = tab[lin+x][col+y]
                            except IndexError:
                                continue
                            else:
                                if pos == 1:
                                    possiveisSaltos = possiveisSaltos+1    #Se no final da verificação, a variável for igual a 1, isso indica que só tinha um local
                    if possiveisSaltos == 1:    #de onde podia se realizar o salto, então a função vai procurar esse lugar para transforma o valor dessa casa para 0
                        try:
                            if lin-3<0 or col-1<0:
                                raise IndexError
                            saltoCim = tab[lin-3][col-1]
                        except IndexError:
                            pass
                        else:
                            if saltoCim == 1:
                                tab[lin-3][col-1] = 0
                        try:
                            if lin+1<0 or col-1<0:
                                raise IndexError
                            saltoBai = tab[lin+1][col-1]
                        except IndexError:
                            pass
                        else:
                            if saltoBai == 1:
                                tab[lin+1][col-1] = 0
                        try:
                            if lin-1<0 or col+1<0:
                                raise IndexError
                            saltoDir = tab[lin-1][col+1]
                        except IndexError:
                            pass
                        else:
                            if saltoDir == 1:
                                tab[lin-1][col+1] = 0
                        try:
                            if lin-1<0 or col-3<0:
                                raise IndexError
                            saltoEsq = tab[lin-1][col-3]
                        except IndexError:
                            pass
                        else:
                            if saltoEsq == 1:
                                tab[lin-1][col-3] = 0
                    else:    #Mas agora, se a variável tiver valor maior que 1, isso indica que tinha mais de um local de onde o jogador podia saltar
                        print('Parece que ha mais de um lugar de onde voce pode saltar.')
                        while True:    #Então o jogador vai entrar nesse while para selecionar de qual casa ele queria pular
                            try:
                                linSal = int(input('Insira a linha de onde quer saltar: '))
                                colSal = int(input('Insira a coluna de onde quer saltar: '))
                            except ValueError:
                                print('Por favor, insira uma posicao valida.')
                            else:
                                if tab[linSal-1][colSal-1] == 1 and (linSal-1 == lin-3 and colSal-1 == col-1):
                                    tab[lin-3][col-1] = 0
                                    break
                                elif tab[linSal-1][colSal-1] == 1 and (linSal-1 == lin+1 and colSal-1 == col-1):
                                    tab[lin+1][col-1] = 0
                                    break
                                elif tab[linSal-1][colSal-1] == 1 and (linSal-1 == lin-1 and colSal-1 == col+1):
                                    tab[lin-1][col+1] = 0
                                    break
                                elif tab[linSal-1][colSal-1] == 1 and (linSal-1 == lin-1 and colSal-1 == col-3):
                                    tab[lin-1][col-3] = 0
                                    break
                                else:
                                    print('Por favor, insira uma posicao valida.')
                    
                    break    #Aqui acaba a vez do jogador 1, se repitindo tudo para o jogador 2
            print('==========================')
        for lin in range(8):
            for col in range(8):
                if tab[lin][col] == 'X':
                    tab[lin][col] = 0
        vezJogador = 2
        jogador = 2
        verificacao = verPossivelContinuar(tab,jogador)
        if verificacao == 0:
            break
        print('{}, seu turno!'.format(j2))
        print('==========================')
        if vezJogador == 2:
            for lin in range(1,9):
                for col in range(1,9):
                    pos = verPos(tab,str(lin),str(col),jogador)
                    if pos == 1 or pos == 2:
                        tab[lin-1][col-1] = 'X'
            printPlacar(tab)
            imprimirTab(tab)
            print('==========================')
            while True:
                lin = input('Selecione a linha desejada: ')
                col = input('Selecione a coluna desejada: ')
                if lin.upper() == 'S' or col.upper() == 'S':
                    for lin in range(8):
                        for col in range(8):
                            if tab[lin][col] == 'X':
                                tab[lin][col] = 0
                    vezJogador = 2
                    tf = tm.time()
                    salvarJogo(j1,j2,tab,rodada,tf-t0+tempoAntes,vezJogador)
                    print('==========================')
                    return 0,0,0
                res = verPos(tab,lin,col,jogador)
                if res == 0:
                    print('Por favor, insira uma posicao valida.')
                elif res == 1:
                    lin = int(lin)
                    col = int(col)
                    tab[lin-1][col-1] = 2
                    for x in range(-2,1): 
                        for y in range(-2,1):
                            try:                                                     
                                if (lin+x<0 or lin+x>8) or (col+y<0 or col+y>8):
                                    raise IndexError
                                pos = tab[lin+x][col+y]
                            except IndexError:
                                continue
                            else:
                                if pos == 1:
                                    tab[lin+x][col+y] = 2
                    break
                else:
                    lin = int(lin)
                    col = int(col)
                    tab[lin-1][col-1] = 2
                    possiveisSaltos = 0
                    for x in range(-2,1):
                        for y in range(-2,1):
                            try:
                                if (lin+x<0 or lin+x>8) or (col+y<0 or col+y>8):
                                    raise IndexError
                                pos = tab[lin+x][col+y]
                            except IndexError:
                                continue
                            else:
                                if pos == 1:
                                    tab[lin+x][col+y] = 2
                    for x in [-3,-1,1]:
                        for y in [-3,-1,1]:
                            if (x == -3 and y == -3) or (x == -3 and y == 1) or\
                               (x == 1 and y == -3) or (x == 1 and y == 1) or (x == -1 and y == -1):
                                continue
                            try:
                                if lin+x<0 or lin+x>7 or col+y<0 or col+y>7:
                                    raise IndexError
                                pos = tab[lin+x][col+y]
                            except IndexError:
                                pass
                            else:
                                if pos == 2:
                                    possiveisSaltos = possiveisSaltos+1
                    if possiveisSaltos == 1:
                        try:
                            if lin-3<0 or col-1<0:
                                raise IndexError
                            saltoCim = tab[lin-3][col-1]
                        except IndexError:
                            pass
                        else:
                            if saltoCim == 2:
                                tab[lin-3][col-1] = 0
                        try:
                            if lin+1<0 or col-1<0:
                                raise IndexError
                            saltoBai = tab[lin+1][col-1]
                        except IndexError:
                            pass
                        else:
                            if saltoBai == 2:
                                tab[lin+1][col-1] = 0
                        try:
                            if lin-1<0 or col+1<0:
                                raise IndexError
                            saltoDir = tab[lin-1][col+1]
                        except IndexError:
                            pass
                        else:
                            if saltoDir == 2:
                                tab[lin-1][col+1] = 0
                        try:
                            if lin-1<0 or col-3<0:
                                raise IndexError
                            saltoEsq = tab[lin-1][col-3]
                        except IndexError:
                            pass
                        else:
                            if saltoEsq == 2:
                                tab[lin-1][col-3] = 0
                    else:
                        print('Parece que ha mais de um lugar de onde voce pode saltar.')
                        while True:
                            try:
                                linSal = int(input('Insira a linha de onde quer saltar: '))
                                colSal = int(input('Insira a coluna de onde quer saltar: '))
                            except ValueError:
                                print('Por favor, insira uma posicao valida.')
                            else:
                                if tab[linSal-1][colSal-1] == 2 and (linSal-1 == lin-3 and colSal-1 == col-1):
                                    tab[lin-3][col-1] = 0
                                    break
                                elif tab[linSal-1][colSal-1] == 2 and (linSal-1 == lin+1 and colSal-1 == col-1):
                                    tab[lin+1][col-1] = 0
                                    break
                                elif tab[linSal-1][colSal-1] == 2 and (linSal-1 == lin-1 and colSal-1 == col+1):
                                    tab[lin-1][col+1] = 0
                                    break
                                elif tab[linSal-1][colSal-1] == 2 and (linSal-1 == lin-1 and colSal-1 == col-3):
                                    tab[lin-1][col-3] = 0
                                    break
                                else:
                                    print('Por favor, insira uma posicao valida.')
                                     
                    break
                print('==========================')
        for lin in range(8):
            for col in range(8):
                if tab[lin][col] == 'X':
                    tab[lin][col] = 0
        rodada = rodada + 1    #Depois de repetir tudo para o jogador 2, acrescenta mais 1 ao valor da rodada
        vezJogador = 1    #e a vezJogador volta a ser 1
    for lin in range(8):
        for col in range(8):
           if tab[lin][col] == 'X':
                tab[lin][col] = 0
    tab = preencherTab(tab)   #Quando a função chega até aqui isso indica que algum jogador não tinha mais como continuar, então a função sai do loop e chama a função preencherTab para ocupar as casas que ainda podiam ser ocupadas pelo outro jogdor
    tf = tm.time()    #Tempo final da partida, então para encontrar o tempo de partida basta fazer tf - t0
    pontosJ1 = 0
    pontosJ2 = 0
    for linha in tab:    #Aqui vai ser realizado a contagem dos pontos
        for num in linha:
            if num == 1:
                pontosJ1 = pontosJ1+1
            elif num == 2:
                pontosJ2 = pontosJ2+1
    if pontosJ1 > pontosJ2:    #E aqui, vai montar as listas de acordo com quem ganhou (se houver ganhador)
        print('Parabens {}, voce foi o grande vencedor!'.format(j1))
        ganhadorJ1 = 1
        ganhadorJ2 = 0
        dadosPartida = ['G',j1,j2,pontosJ1,pontosJ2,tf-t0+tempoAntes]
    elif pontosJ1 < pontosJ2:
        print('Parabens {}, voce foi o grande vencedor!'.format(j2))
        ganhadorJ1 = 0
        ganhadorJ2 = 1
        dadosPartida = ['G',j2,j1,pontosJ2,pontosJ1,tf-t0+tempoAntes]
    else:
        print('Os dois fizeram a mesma quantidade de pontos, entao o jogo empatou!')
        ganhadorJ1 = 0
        ganhadorJ2 = 0
        dadosPartida = ['E',j1,j2,pontosJ1,pontosJ2,tf-t0+tempoAntes]
    dadosJ1 = [j1,1,ganhadorJ1,pontosJ1,tf-t0+tempoAntes,tf-t0+tempoAntes]    #E aqui é a lista com os dados de cada jogador
    dadosJ2 = [j2,1,ganhadorJ2,pontosJ2,tf-t0+tempoAntes,tf-t0+tempoAntes]
    print('==========================')
    return dadosJ1,dadosJ2,dadosPartida    #Retornando no final os dados dos jogadores e da partida


    

                
def main():    #Essa função vai funcionar como o menu do jogo
    print('Seja bem-vindo ao Dominate')
    print('==========================')
    while True:  #Loop para manter o jogador no menu ate que queira sair
        print('1 - Iniciar novo jogo.')
        print('2 - Carregar ultimo jogo.')
        print('3 - Estatisticas dos jogadores.')
        print('4 - Historico de partidas.')
        print('5 - Sair.')
        print('==========================')
        r = input('Escolha uma das opções acima: ')
        if r == '1':
            dJ1,dJ2,dPartida = dominate(0)
            if dJ1 != 0:    #O retorno da função 0,0,0 é importante para a função não tentar escrever os dados de um jogador ou de uma partida que não foram finalizadas
                alterarDadosJogs(dJ1)     #Mas se a partida foi finalizada, vai ser realizada a chamada da função alterarDadosJogs para alterar os dados do jogador ou acrescentar um jogador
                alterarDadosJogs(dJ2)
                historico(dPartida)    #A chamada da função histórico vai salvar os resultados da partida em um arquivo
        elif r == '2':     
            try:    #Aqui é para quando for tentar carregar um jogo
                arq = open('Save.txt','r')
            except FileNotFoundError:
                print('Nao ha nenhum jogo salvo.')    #Se não houver nenhum jogo salvo, vai ser impresso a mensagem do "print" e a função volta para o menu
            else:    #Mas se houver um save, vai ser realizado a chamada da função dominate, porem com arq = 1 indicando que é para iniciar o jogo no arquivo.txt
                arq.close()
                dJ1,dJ2,dPartida = dominate(1)
                if dJ1 != 0:   #if com o mesmo motivo do de cima
                    alterarDadosJogs(dJ1)
                    alterarDadosJogs(dJ2)
                    historico(dPartida)
                    os.remove('Save.txt')    #O único diferencial é esse os.remove que vai deletar o save quando o jogo for finalizado
        elif r == '3':
            try:    #Aqui, é para quando for carregar os dados dos jogadores
                arq = open('DadosJogs.txt','r')
            except FileNotFoundError:    #Se não houver nenhum dado, a função vai imprimir a mensagem do print na tela e voltar para o menu
                print('Nenhum jogador encontrado.')
            else:    #Mas, existindo dados de jogadores, a função vai mostrar o dado de cada jogador no arquivo
                print('Aqui estao os jogadores')
                print('==========================')
                linha = arq.readline()
                while len(linha) != 0:    #Esse loop serve para a função imprimir cada linha do arquivo até na existir mais dados, ou seja, chegar em uma linha com len = 0
                    linha = linha[:-2]
                    lista = linha.split(',')
                    print('Jogador: {}, Partidas: {}, Vitorias: {}, Pontuacao maxima: {}, Tempo maximo: {}m{}s, Tempo minimo: {}m{}s'.format(lista[0],lista[1],lista[2],lista[3],(int(float(lista[4])//60)),(int(float(lista[4])%60)),(int(float(lista[5])//60)),(int(float(lista[5])%60))))
                    linha = arq.readline()
                    print('==========================')
                arq.close()
        elif r == '4':
            try:    #Mesma coisa que as outras opções, se não houver histórico de partidas, vai aparecer uma mensagem falando que não há partidas
                partidas = open('DadosPartida.txt','r')
            except FileNotFoundError:
                print('Nenhuma partida encontrada.')
            else:    #Porém, tendo um histórico, a função vai imprimir as 10 partidas mais recentes
                print('Partidas encontradas:')
                print('==========================')
                listaPart = partidas.readlines()
                numPart = -1    #Essa variável vai fazer com que a função pegue as partidas da ultima até a primeira na lista
                while numPart >= -10:     #Isso porque as partidas mais recentes são as últimas
                    try:
                        part = listaPart[numPart][:-2]
                        part = part.split(',')
                    except:    #Esse except é só para se houver algum erro que não previ
                        numPart = numPart-1
                        continue
                    else:
                        if part[0] == 'G':    #Aqui vai entrar aquele "G" ou "E" da lista que retorna a função dominate 
                            print('Partida: {} vs {}.'.format(part[1],part[2]))
                            print('Ganhador: {}, Pontuacao: {} a {}, Tempo: {}m{}s'.format(part[1],part[3],part[4],(int(float(part[5])//60)),(int(float(part[5])%60))))
                            print('==========================')
                        else:
                            print('Partida: {} vs {}.'.format(part[1],part[2]))
                            print('Ganhador: Empate, Pontuacao: {} a {}, Tempo: {}m{}s'.format(part[3],part[4],(int(float(part[5])//60)),(int(float(part[5])%60))))
                            print('==========================')
                        numPart = numPart-1
                partidas.close()
                        
        elif r == '5':    #Aqui é só uma mensagem de agardecimento para quem está jogando
            print('Obrigado por jogar!')
            break
        else:    #Esse else serve para se o jogador digita uma opção ou alguma outra coisa que não exista não dar erro
            print('Digite uma opcao valida.')
            print('==========================')
    return 0

if __name__ == '__main__':    #Alguns dos testes feitos
    print('Funcao verPos:')
    print(verPos([[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]],'5','5',1))
    print(verPos([[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]],'5','5',2))
    print(verPos([[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]],'1','3',1))
    print(verPos([[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]],'1','6',2))
    print(verPos([[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]],'1','2',1))
    print(verPos([[1,0,0,0,0,0,0,2],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],\
                  [0,0,0,0,0,0,0,0],[2,0,0,0,0,0,0,1]],'8','2',2))
    print('Funcao verPossivelContinuar:')
    print(verPossivelContinuar([[1,0,1,1,2,2,2,2],[1,1,1,2,2,2,2,2],[1,1,1,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]],2))
    print(verPossivelContinuar([[1,0,1,1,2,2,2,2],[1,1,1,2,2,2,2,2],[1,1,1,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]],1))
    print(verPossivelContinuar([[1,0,1,2,2,2,2,2],[1,1,1,2,2,2,2,2],[1,1,1,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]],2))
    print('Funcao preencherTab:')
    print(preencherTab([[1,0,1,1,2,2,2,2],[1,1,1,2,2,2,2,2],[1,1,1,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2],\
                  [2,2,2,2,2,2,2,2],[2,2,2,2,2,2,2,2]]))
    print(preencherTab([[1,1,1,1,1,1,1,1],[1,1,2,2,2,2,1,1],[1,1,2,2,2,2,1,1],\
                  [1,2,2,2,2,2,2,1],[2,2,0,0,0,0,2,2],[2,0,0,0,0,0,0,2],\
                  [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]))

main()